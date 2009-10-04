"""
Tests for grouping functionality in Gaphor.
"""

from gaphor import UML
from gaphor.diagram import items
from gaphor.diagram.interfaces import IGroup
from zope import component

from gaphor.tests import TestCase 

class NodeComponentGroupTestCase(TestCase):
    def group(self, parent, item):
        """
        Group item within a parent.
        """
        query = (parent, item)
        adapter = component.queryMultiAdapter(query, IGroup)
        adapter.group()


    def ungroup(self, parent, item):
        """
        Remove item from a parent.
        """
        query = (parent, item)
        adapter = component.queryMultiAdapter(query, IGroup)
        adapter.ungroup()


    def test_grouping(self):
        """Test component within node composition
        """
        n = self.create(items.NodeItem, UML.Node)
        c = self.create(items.ComponentItem, UML.Component)

        self.group(n, c)

        self.assertEquals(1, len(n.subject.ownedAttribute))
        self.assertEquals(1, len(n.subject.ownedConnector))
        self.assertEquals(1, len(c.subject.ownedAttribute))
        self.assertEquals(2, len(self.kindof(UML.ConnectorEnd)))

        a1 = n.subject.ownedAttribute[0]
        a2 = c.subject.ownedAttribute[0]

        self.assertTrue(a1.isComposite)
        self.assertTrue(a1 in n.subject.part)

        connector = n.subject.ownedConnector[0]
        self.assertTrue(connector.end[0].role is a1)
        self.assertTrue(connector.end[1].role is a2)


    def test_ungrouping(self):
        """Test decomposition of component from node
        """
        n = self.create(items.NodeItem, UML.Node)
        c = self.create(items.ComponentItem, UML.Component)

        query = self.group(n, c)
        query = self.ungroup(n, c)

        self.assertEquals(0, len(n.subject.ownedAttribute))
        self.assertEquals(0, len(c.subject.ownedAttribute))
        self.assertEquals(0, len(self.kindof(UML.Property)))
        self.assertEquals(0, len(self.kindof(UML.Connector)))
        self.assertEquals(0, len(self.kindof(UML.ConnectorEnd)))

