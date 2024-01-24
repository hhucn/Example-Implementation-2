from neomodel import StructuredNode, StringProperty, ArrayProperty, RelationshipTo, UniqueIdProperty, IntegerProperty 


class Comment(StructuredNode):
    """
    Neomodel structured node that defines the properties for the comments that are stored in the Neo4J database
    """
    comment_id = UniqueIdProperty()
    text = StringProperty()
    embedding = ArrayProperty()
    up_votes = IntegerProperty()

    article = RelationshipTo('.article.Article', 'BELONGS_TO')
