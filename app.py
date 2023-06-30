from flask import Flask, jsonify, request

app = Flask(__name__)

class TreeNode:
    def __init__(self, dimension_key, dimension_value):
        self.dimension_key = dimension_key
        self.dimension_value = dimension_value
        self.metric_values = {}
        self.children = []

    def update_metrics(self, metrics):
        for metric_key, metric_value in metrics.items():
            self.metric_values[metric_key] = self.metric_values.get(metric_key, 0) + metric_value

    def add_child(self, child):
        self.children.append(child)


class Tree:
    def __init__(self):
        self.root = TreeNode("", "")

    def insert_data(self, dimensions, metrics):
        current_node = self.root

        for dimension in dimensions:
            dimension_key = dimension["key"]
            dimension_value = dimension["val"]

            matching_child = next(
                (child for child in current_node.children if child.dimension_value == dimension_value), None
            )

            if matching_child:
                current_node = matching_child
            else:
                new_node = TreeNode(dimension_key, dimension_value)
                current_node.add_child(new_node)
                current_node = new_node

        current_node.update_metrics(metrics)

    def aggregate_metrics(self, node):
        aggregated_metrics = {}
        for child in node.children:
            child_metrics = self.aggregate_metrics(child)
            for metric_key, metric_value in child_metrics.items():
                aggregated_metrics[metric_key] = aggregated_metrics.get(metric_key, 0) + metric_value
        aggregated_metrics.update(node.metric_values)
        return aggregated_metrics

    def dump_tree(self):
        self._dump_node(self.root)

    def _dump_node(self, node, indent=""):
        print(f"{indent}{node.dimension_key}: {node.dimension_value}")
        for metric_key, metric_value in node.metric_values.items():
            print(f"{indent}  {metric_key}: {metric_value}")
        for child in node.children:
            self._dump_node(child, indent + "  ")


tree = Tree()

@app.route('/v1/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    dimensions = data.get('dim', [])
    metrics = {metric['key']: metric['val'] for metric in data.get('metrics', [])}
    tree.insert_data(dimensions, metrics)
    return jsonify({"message": "Data inserted successfully."}), 200

@app.route('/v1/query', methods=['POST'])
def query_data():
    data = request.get_json()
    dimensions = data.get('dim', [])

    current_node = tree.root
    for dimension in dimensions:
        dimension_value = dimension["val"]
        matching_child = next(
            (child for child in current_node.children if child.dimension_value == dimension_value), None
        )
        if matching_child:
            current_node = matching_child
        else:
            return jsonify({"message": "No data found for the specified dimensions."}), 200

    aggregated_metrics = tree.aggregate_metrics(current_node)

    return jsonify(aggregated_metrics), 200


if __name__ == '__main__':
    app.run()
