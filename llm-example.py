import pm4py


def execute_script():
    """
    Generates some hypothesis for the analysis of an event log starting
    from the process variants and log attributes abstraction of the event log.
    The hypothesis shall come with a DuckDB SQL query that can be verified against the dataframe
    """
    log = pm4py.read_xes("./preprocessed_data/08_Activity+Location/S09.xes")
    prompt = []
    prompt.append("\n\nIf I have the following process variants:\n")
    prompt.append(pm4py.llm.abstract_variants(log, max_len=3000, response_header=False))
    prompt.append("\n\nand attributes in the log:\n")
    prompt.append(pm4py.llm.abstract_log_attributes(log, max_len=3000))
    prompt.append("\n\n")
    prompt = "".join(prompt)
    
    net, st, fi = pm4py.read_pnml('./output.pnml')
    fi = ['sink:1']
    print(pm4py.llm.abstract_petri_net(net, st, fi))


if __name__ == "__main__":
    execute_script()