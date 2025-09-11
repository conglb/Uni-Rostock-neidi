



def remove_skip_connections(net):
    # Remove nodes (places or transitions) whose name starts with "skip"
    nodes_to_remove = []

    for place in net.places:
        if place.name and place.name.startswith("skip"):
            nodes_to_remove.append(place)

    for transition in net.transitions:
        if transition.label and transition.label.startswith("skip"):
            nodes_to_remove.append(transition)

    # Disconnect and remove the nodes from the net
    for node in nodes_to_remove:
        # Remove all arcs connected to the node
        for arc in list(node.in_arcs):
            net.remove_arc(arc)
        for arc in list(node.out_arcs):
            net.remove_arc(arc)
        # Remove node from the net
        if node in net.places:
            net.places.remove(node)
        if node in net.transitions:
            net.transitions.remove(node)

