

class TransformationRule:
    def __init__(self, LHS, RHS, mapping_L_to_R):
        self.LHS = LHS  # PetriNet pattern
        self.RHS = RHS  # PetriNet replacement
        self.mapping = mapping_L_to_R  # dict: LHS node -> RHS node


    def apply(self, net, initial_marking, final_marking):
        """
        Apply the transformation rule to a given Petri net.
        :param net: The Petri net to be transformed.
        :param initial_marking: The initial marking of the Petri net.
        :param final_marking: The final marking of the Petri net.
        :return: The transformed Petri net, initial marking, and final marking.
        """
        # Create a copy of the original Petri net
        new_net = net.copy()
        new_initial_marking = initial_marking.copy()
        new_final_marking = final_marking.copy()

        # Apply the transformation rule
        for lhs_node, rhs_node in self.mapping.items():
            # Replace LHS node with RHS node in the Petri net
            if lhs_node in new_net.places:
                new_net.places.remove(lhs_node)
                new_net.places.add(rhs_node)
            elif lhs_node in new_net.transitions:
                new_net.transitions.remove(lhs_node)
                new_net.transitions.add(rhs_node)

        return new_net, new_initial_marking, new_final_marking
    
    def check_match(self, net):
        """
        Check if the transformation rule matches a given subnet.
        :param net: The Petri net to be checked.
        :return: True if the rule matches, False otherwise.
        """
        # Check if the LHS pattern matches the net
        for lhs_node in self.LHS:
            if lhs_node not in net.places and lhs_node not in net.transitions:
                return False
        return True