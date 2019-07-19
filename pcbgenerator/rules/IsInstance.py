from dxfgrabber.dxfentities import DXFEntity


class IsInstance:
    """
    This rule checks that entity is of the given instance.
    """

    def __init__(self, type):
        """

        :param type:
        :type type: type
        """
        self.type = type
        pass

    def __call__(self, entity):
        """

        :param entity:
        :type entity: DXFEntity
        :return:
        :rtype: bool
        """
        return entity is type