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
    RETURN w.name as WP, w.lead_institute as lead, w.wp as id, COUNT(distinct p) as Individuals,
    COUNT(distinct n) as Organizations"""


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


def get_skill_group():
    return """MATCH (n:SkillGroup)
    RETURN n.name as SkillGroup"""


def skill_distribution():
    return """MATCH path=(s1)-[q]->(s2: Skill)<-[]-(p:Person)
    WITH nodes(path) as no
    WITH no, last(no) as leaf
    WITH  [n IN no[..-1] | n.name] AS Skills, count(distinct leaf.name) as Individuals
    RETURN Skills[0] as name, Skills[1] as skill_name, Individuals"""


def skill_metadata():
    return """MATCH (n:SkillGroup)-[]->(s:Skill)
    RETURN n.name as SkillGroup, s.name as Skill, s.curie as Curie, s.info as description, s.info_link as url"""


def get_skill_info():
    return """MATCH path=(s1:SkillGroup)-[]->(s2: Skill)<-[]-(p:Person)-[]->(i:Partner)
    RETURN s1.name as Group, s2.name as Skill, p.name as Individual, p.info as ORCID, i.name as Affiliation"""


def get_all_assays():
    return """MATCH (e:Experiment)
    RETURN e.name as Assay, e.curie as Curie, e.definition as Definition"""


def get_all_software():
    return """MATCH (s:Software)
    RETURN s.name as Software, s.curie as Curie"""


def get_all_target_classes():
    return """MATCH (t:TargetClass)
    RETURN t.name as Target, t.curie as Curie"""


def get_tech_info(name: str):
    """Get the technology information. The name could be software, assay, or target class"""
    return f"""MATCH path=(e)-[q]->(i: Partner)<-[]-(p:Person)
    WHERE e.name = '{name}' 
    WITH nodes(path) as no
    WITH no, last(no) as leaf
    WITH  [n IN no[..-1] | n.name] AS Partner, count(distinct leaf.name) as Percentage
    RETURN e.name, Partner[0] as info, Partner[1] as Partner, Percentage"""


def get_tech_data(class_type: str):
    """Get the technology information. The name could be software, assay, or target class"""
    assert class_type in ["Software", "Experiment", "TargetClass"], "Invalid class type"
    return f"""MATCH path=(e: {class_type})-[q]->(i: Partner)<-[]-(p:Person)
    RETURN e.name as Name, p.name as info, i.name as Partner"""


def get_partner_info():
    return """MATCH (p:Partner)
    RETURN p.name as Name, p.location as Location, p.acronym as acronym, p.info as info_link"""


def get_person_info():
    return """MATCH (p:Person)-[]->(i:Partner)
    RETURN i.name as Partner, p.name as Name, p.info as ORCID"""


def get_all_partner_relationships():
    return """MATCH (p)-[]-(i:Partner)
    WHERE not labels(p) = ['Person']
    RETURN p.name as Name, i.name as Partner"""
