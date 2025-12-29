from eunoia.lhr.state import LogicalState


def compile_rts_to_state(rts):
    state = LogicalState()

    state.variables = rts["variables"]
    state.inputs = rts.get("inputs", [])
    state.outputs = rts.get("outputs", [])
    state.effects = rts.get("effects", [])
    state.causes = rts.get("causes", [])
    state.estimated = rts.get("estimate")
    state.calculated = rts.get("result")

    return state
