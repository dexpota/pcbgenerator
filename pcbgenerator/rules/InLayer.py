from dxfgrabber.dxfentities import DXFEntity


class InLayer:
    """
    This rule checks that entity is of the given instance.
    """

    def __init__(self, layer):
        """

        :param layer:
        :type layer: str
        """
        self.layer = layer
        pass

    def __call__(self, entity):
        """

        :param entity:
        :type entity: DXFEntity
        :return:
        :rtype: bool
        """
        return entity.layer == self.layer
