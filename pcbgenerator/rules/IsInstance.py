from dxfgrabber.dxfentities import DXFEntity


class IsInstance:
    """
    This rule checks that entity is of the given instance.
    """

    def __init__(self, t):
        """

        :param type:
        :type type: type
        """
        self.t = t
        pass

    def __call__(self, entity):
        """

        :param entity:
        :type entity: DXFEntity
        :return:
        :rtype: bool
        """
        return type(entity) == self.t
