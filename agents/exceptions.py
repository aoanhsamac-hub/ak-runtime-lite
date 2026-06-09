class AgentRuntimeError(Exception):
    pass


class AgentAuthorityError(AgentRuntimeError):
    pass


class AgentLifecycleError(AgentRuntimeError):
    pass
