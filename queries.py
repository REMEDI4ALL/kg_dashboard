def get_location():
    return """MATCH (p:Partner)
    CALL {
        WITH p
        RETURN p.location as Location, count(*) as value
    }
    WITH Location, sum(value) as `Partner counts`
    RETURN Location, `Partner counts`"""


def get_organization_info():
    return """MATCH (p:Person)-[]->(i:Partner)
    RETURN i.name as Partner, COUNT(distinct p) as Individuals
    """


def get_wp_info():
    return """MATCH (n:Partner)<-[e]-(p:Person)-[i]->(w:WP)
    RETURN w.name as WP, w.leaders as lead, w.wp as id, COUNT(distinct p) as Individuals"""


def get_node_counts():
    return """MATCH (n)
    WHERE not n.name = '_Neodash_Dashboard'
    RETURN COUNT(n)"""


def get_edge_counts():
    return """MATCH (n)-[r]-(t)
    RETURN COUNT(distinct r)"""


def get_node_stats():
    return """CALL db.labels() YIELD label
    CALL apoc.cypher.run('MATCH (:`'+label+'`) RETURN count(*) as count',{}) YIELD value
    WHERE NOT label IN ['_Neodash_Dashboard', 'SkillGroup']
    RETURN label as Nodes, value.count as Counts"""
