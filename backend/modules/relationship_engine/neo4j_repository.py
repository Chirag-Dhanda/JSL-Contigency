import logging
from typing import Dict, Any, List
from database.neo4j_engine import Neo4jEngine
from neo4j import AsyncSession

logger = logging.getLogger("Neo4jRepository")

class Neo4jRepository:
    """Executes Cypher queries against Neo4j to manage the graph projection."""

    async def _get_session(self) -> AsyncSession:
        return Neo4jEngine.get_driver().session()

    async def upsert_node(self, node_id: str, labels: List[str], properties: Dict[str, Any]):
        """Creates or updates a node with dynamic labels and properties."""
        label_str = ":".join(labels) if labels else "Entity"
        # We can't parameterize labels in cypher, so we use string interpolation for labels.
        # It's safe here because labels come from our own trusted Ontology registry.
        query = f"""
        MERGE (n:Entity {{id: $node_id}})
        SET n:{label_str}
        SET n += $properties
        """
        try:
            async with await self._get_session() as session:
                await session.run(query, node_id=node_id, properties=properties)
                logger.debug(f"Upserted Node {node_id} with labels {labels}")
        except Exception as e:
            logger.error(f"Neo4j Upsert Node Failed for {node_id}: {e}")

    async def delete_node(self, node_id: str):
        query = """
        MATCH (n:Entity {id: $node_id})
        DETACH DELETE n
        """
        try:
            async with await self._get_session() as session:
                await session.run(query, node_id=node_id)
        except Exception as e:
            logger.error(f"Neo4j Delete Node Failed for {node_id}: {e}")

    async def upsert_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Dict[str, Any]):
        """Creates or updates a directed relationship between two nodes."""
        query = f"""
        MATCH (a:Entity {{id: $source_id}})
        MATCH (b:Entity {{id: $target_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $properties
        """
        try:
            async with await self._get_session() as session:
                await session.run(query, source_id=source_id, target_id=target_id, properties=properties)
                logger.debug(f"Upserted Relationship {source_id} -[{rel_type}]-> {target_id}")
        except Exception as e:
            logger.error(f"Neo4j Upsert Relationship Failed: {e}")

    async def delete_relationship(self, source_id: str, target_id: str, rel_type: str):
        query = f"""
        MATCH (a:Entity {{id: $source_id}})-[r:{rel_type}]->(b:Entity {{id: $target_id}})
        DELETE r
        """
        try:
            async with await self._get_session() as session:
                await session.run(query, source_id=source_id, target_id=target_id)
        except Exception as e:
            logger.error(f"Neo4j Delete Relationship Failed: {e}")

    async def get_neighbors(self, node_id: str, max_depth: int = 1) -> List[Dict[str, Any]]:
        """Finds neighbor nodes up to max_depth."""
        query = """
        MATCH p=(n:Entity {id: $node_id})-[*1..""" + str(max_depth) + """]-(m)
        RETURN [x IN nodes(p) | properties(x)] AS path_nodes,
               [r IN relationships(p) | {type: type(r), props: properties(r)}] AS path_rels
        """
        paths = []
        try:
            async with await self._get_session() as session:
                result = await session.run(query, node_id=node_id)
                async for record in result:
                    paths.append({
                        "nodes": record["path_nodes"],
                        "relationships": record["path_rels"]
                    })
        except Exception as e:
            logger.error(f"Neo4j Traversal Failed: {e}")
        return paths
