import os
import zipfile

base_dir = "/tmp/context_reasoner_bundle"
os.makedirs(base_dir, exist_ok=True)

files = {
    # ---------------- JAVA ----------------
    "java/pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>org.example.aaa</groupId>
  <artifactId>priority-context-reasoner</artifactId>
  <version>1.0.0</version>

  <properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <jena.version>5.6.0</jena.version>
    <owlapi.version>4.5.29</owlapi.version>
    <elk.version>0.6.0</elk.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.apache.jena</groupId>
      <artifactId>apache-jena-libs</artifactId>
      <version>${jena.version}</version>
      <type>pom</type>
    </dependency>
    <dependency>
      <groupId>net.sourceforge.owlapi</groupId>
      <artifactId>owlapi-distribution</artifactId>
      <version>${owlapi.version}</version>
    </dependency>
    <dependency>
      <groupId>io.github.liveontologies</groupId>
      <artifactId>elk-owlapi</artifactId>
      <version>${elk.version}</version>
    </dependency>
  </dependencies>
</project>
""",

    "java/src/main/java/org/example/aaa/FocusedSubgraphExtractor.java": """package org.example.aaa;

import java.util.*;
import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.*;

public class FocusedSubgraphExtractor {

    private static final Property OWL_ON_PROPERTY =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#onProperty");
    private static final Property OWL_SOME_VALUES_FROM =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#someValuesFrom");
    private static final Property OWL_ALL_VALUES_FROM =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#allValuesFrom");
    private static final Property OWL_HAS_VALUE =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#hasValue");
    private static final Property OWL_ON_CLASS =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#onClass");
    private static final Property OWL_EQUIVALENT_CLASS =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#equivalentClass");
    private static final Property OWL_EQUIVALENT_PROPERTY =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#equivalentProperty");
    private static final Property OWL_INVERSE_OF =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#inverseOf");
    private static final Property OWL_INTERSECTION_OF =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#intersectionOf");
    private static final Property OWL_UNION_OF =
        ResourceFactory.createProperty("http://www.w3.org/2002/07/owl#unionOf");

    public Model extractFocusedSubgraph(
            Model source,
            Set<Resource> focusClasses,
            Set<Property> focusProperties,
            boolean includeSubClasses,
            int maxIterations) {

        Set<RDFNode> relevantNodes = new LinkedHashSet<>();
        relevantNodes.addAll(focusClasses);
        relevantNodes.addAll(focusProperties);

        for (int iter = 0; iter < maxIterations; iter++) {
            Set<RDFNode> newlyAdded = new LinkedHashSet<>();

            for (RDFNode node : relevantNodes) {
                if (!(node instanceof Resource res)) {
                    continue;
                }

                collectRelatedObjects(source, res, RDFS.subClassOf, newlyAdded);
                collectRelatedObjects(source, res, OWL_EQUIVALENT_CLASS, newlyAdded);
                collectRelatedSubjects(source, res, OWL_EQUIVALENT_CLASS, newlyAdded);

                if (includeSubClasses) {
                    collectRelatedSubjects(source, res, RDFS.subClassOf, newlyAdded);
                }

                collectRelatedObjects(source, res, RDFS.subPropertyOf, newlyAdded);
                collectRelatedObjects(source, res, OWL_EQUIVALENT_PROPERTY, newlyAdded);
                collectRelatedSubjects(source, res, OWL_EQUIVALENT_PROPERTY, newlyAdded);
                collectRelatedObjects(source, res, OWL_INVERSE_OF, newlyAdded);
                collectRelatedSubjects(source, res, OWL_INVERSE_OF, newlyAdded);
                collectRelatedObjects(source, res, RDFS.domain, newlyAdded);
                collectRelatedObjects(source, res, RDFS.range, newlyAdded);

                collectMatchingRestrictions(source, res, newlyAdded);
                collectListAndExpressionNodes(source, res, newlyAdded);
            }

            newlyAdded.removeAll(relevantNodes);
            if (newlyAdded.isEmpty()) {
                break;
            }
            relevantNodes.addAll(newlyAdded);
        }

        Model sub = ModelFactory.createDefaultModel();
        Set<Resource> blankNodesToCopy = new LinkedHashSet<>();

        StmtIterator it = source.listStatements();
        while (it.hasNext()) {
            Statement s = it.nextStatement();
            boolean touchesRelevant =
                relevantNodes.contains(s.getSubject()) ||
                relevantNodes.contains(s.getPredicate()) ||
                relevantNodes.contains(s.getObject());

            if (touchesRelevant) {
                sub.add(s);
                if (s.getSubject().isAnon()) {
                    blankNodesToCopy.add(s.getSubject());
                }
                if (s.getObject().isResource() && s.getObject().asResource().isAnon()) {
                    blankNodesToCopy.add(s.getObject().asResource());
                }
            }
        }

        for (Resource bnode : blankNodesToCopy) {
            copyBlankNodeClosure(source, bnode, sub, new HashSet<>());
        }

        return sub;
    }

    private void collectRelatedObjects(Model m, Resource subj, Property pred, Set<RDFNode> out) {
        StmtIterator it = m.listStatements(subj, pred, (RDFNode) null);
        while (it.hasNext()) {
            out.add(it.nextStatement().getObject());
        }
    }

    private void collectRelatedSubjects(Model m, Resource obj, Property pred, Set<RDFNode> out) {
        StmtIterator it = m.listStatements(null, pred, obj);
        while (it.hasNext()) {
            out.add(it.nextStatement().getSubject());
        }
    }

    private void collectMatchingRestrictions(Model m, Resource target, Set<RDFNode> out) {
        Property[] restrictionValueProps = {
            OWL_ON_PROPERTY,
            OWL_SOME_VALUES_FROM,
            OWL_ALL_VALUES_FROM,
            OWL_HAS_VALUE,
            OWL_ON_CLASS
        };

        for (Property prop : restrictionValueProps) {
            StmtIterator it = m.listStatements(null, prop, target);
            while (it.hasNext()) {
                Resource restriction = it.nextStatement().getSubject();
                out.add(restriction);
                collectRelatedObjects(m, restriction, OWL_ON_PROPERTY, out);
                collectRelatedObjects(m, restriction, OWL_SOME_VALUES_FROM, out);
                collectRelatedObjects(m, restriction, OWL_ALL_VALUES_FROM, out);
                collectRelatedObjects(m, restriction, OWL_HAS_VALUE, out);
                collectRelatedObjects(m, restriction, OWL_ON_CLASS, out);
            }
        }
    }

    private void collectListAndExpressionNodes(Model m, Resource node, Set<RDFNode> out) {
        Property[] listProps = { OWL_INTERSECTION_OF, OWL_UNION_OF, RDF.first, RDF.rest };
        for (Property p : listProps) {
            StmtIterator it = m.listStatements(node, p, (RDFNode) null);
            while (it.hasNext()) {
                RDFNode val = it.nextStatement().getObject();
                if (!RDF.nil.equals(val)) {
                    out.add(val);
                }
            }
        }
    }

    private void copyBlankNodeClosure(Model source, Resource bnode, Model target, Set<Resource> visited) {
        if (!bnode.isAnon() || !visited.add(bnode)) {
            return;
        }
        StmtIterator outStmt = source.listStatements(bnode, null, (RDFNode) null);
        while (outStmt.hasNext()) {
            Statement s = outStmt.nextStatement();
            target.add(s);
            if (s.getObject().isResource() && s.getObject().asResource().isAnon()) {
                copyBlankNodeClosure(source, s.getObject().asResource(), target, visited);
            }
        }
    }
}
""",

    "java/src/main/java/org/example/aaa/PriorityContextReasoner.java": """package org.example.aaa;

import java.util.*;
import java.util.concurrent.*;
import org.apache.jena.rdf.model.*;
import org.apache.jena.reasoner.Reasoner;
import org.apache.jena.reasoner.ReasonerRegistry;

public class PriorityContextReasoner {

    public record ContextNode(
        String id,
        int priority,
        Set<Resource> focusClasses,
        Set<Property> focusProperties,
        List<String> dependsOn,
        boolean includeSubClasses,
        int maxClosureIterations
    ) {}

    private final Model baseOntology;
    private final FocusedSubgraphExtractor extractor = new FocusedSubgraphExtractor();
    private final ExecutorService executor;
    private final Map<String, ContextNode> nodes = new LinkedHashMap<>();

    public PriorityContextReasoner(Model baseOntology, int workerThreads) {
        this.baseOntology = baseOntology;
        BlockingQueue<Runnable> queue = new PriorityBlockingQueue<>(
            64,
            (r1, r2) -> Integer.compare(
                ((PrioritizedTask<?>) r1).priority(),
                ((PrioritizedTask<?>) r2).priority()
            )
        );
        this.executor = new ThreadPoolExecutor(
            workerThreads, workerThreads, 0L, TimeUnit.MILLISECONDS, queue
        );
    }

    public void addContext(ContextNode node) {
        nodes.put(node.id(), node);
    }

    public Map<String, CompletableFuture<Model>> runAsync() {
        validateDagNoCycles();
        Map<String, CompletableFuture<Model>> futures = new ConcurrentHashMap<>();
        for (ContextNode node : nodes.values()) {
            computeNodeFuture(node, futures);
        }
        return futures;
    }

    private void validateDagNoCycles() {
        Map<String, Integer> inDegree = new HashMap<>();
        Map<String, List<String>> children = new HashMap<>();

        for (String id : nodes.keySet()) {
            inDegree.put(id, 0);
            children.put(id, new ArrayList<>());
        }
        for (ContextNode node : nodes.values()) {
            for (String parentId : node.dependsOn()) {
                if (!nodes.containsKey(parentId)) {
                    throw new IllegalArgumentException("Unknown parent context: " + parentId);
                }
                inDegree.merge(node.id(), 1, Integer::sum);
                children.get(parentId).add(node.id());
            }
        }

        Deque<String> ready = new ArrayDeque<>();
        for (var entry : inDegree.entrySet()) {
            if (entry.getValue() == 0) {
                ready.add(entry.getKey());
            }
        }

        int visited = 0;
        while (!ready.isEmpty()) {
            String curr = ready.removeFirst();
            visited++;
            for (String childId : children.get(curr)) {
                int rem = inDegree.get(childId) - 1;
                inDegree.put(childId, rem);
                if (rem == 0) {
                    ready.addLast(childId);
                }
            }
        }

        if (visited != nodes.size()) {
            throw new IllegalStateException("Cycle detected in ContextNode priority hierarchy.");
        }
    }

    private CompletableFuture<Model> computeNodeFuture(
            ContextNode node,
            Map<String, CompletableFuture<Model>> futures) {

        if (futures.containsKey(node.id())) {
            return futures.get(node.id());
        }

        List<CompletableFuture<Model>> parentFutures = new ArrayList<>();
        for (String parentId : node.dependsOn()) {
            parentFutures.add(computeNodeFuture(nodes.get(parentId), futures));
        }

        CompletableFuture<Void> allParentsDone = CompletableFuture.allOf(
            parentFutures.toArray(new CompletableFuture[0])
        );

        CompletableFuture<Model> nodeFuture = allParentsDone.thenComposeAsync(ignored -> {
            CompletableFuture<Model> taskFuture = new CompletableFuture<>();
            PrioritizedTask<Model> task = new PrioritizedTask<>(node.priority(), () -> {
                try {
                    Model scopedInput = ModelFactory.createDefaultModel();
                    scopedInput.add(extractor.extractFocusedSubgraph(
                        baseOntology,
                        node.focusClasses(),
                        node.focusProperties(),
                        node.includeSubClasses(),
                        node.maxClosureIterations()
                    ));

                    for (CompletableFuture<Model> pf : parentFutures) {
                        scopedInput.add(pf.join());
                    }

                    Reasoner reasoner = ReasonerRegistry.getOWLReasoner();
                    InfModel inf = ModelFactory.createInfModel(reasoner, scopedInput);
                    inf.prepare();

                    Model inferredOnly = ModelFactory.createDefaultModel();
                    inferredOnly.add(inf.getDeductionsModel());
                    taskFuture.complete(inferredOnly);
                    return inferredOnly;
                } catch (Throwable ex) {
                    taskFuture.completeExceptionally(ex);
                    throw new CompletionException(ex);
                }
            });
            executor.execute(task);
            return taskFuture;
        }, executor);

        futures.put(node.id(), nodeFuture);
        return nodeFuture;
    }

    public void shutdown() {
        executor.shutdown();
    }

    private static final class PrioritizedTask<V> extends FutureTask<V> implements Comparable<PrioritizedTask<?>> {
        private final int priority;

        PrioritizedTask(int priority, Callable<V> callable) {
            super(callable);
            this.priority = priority;
        }

        public int priority() {
            return priority;
        }

        @Override
        public int compareTo(PrioritizedTask<?> other) {
            return Integer.compare(this.priority, other.priority);
        }
    }
}
""",

    "java/src/main/java/org/example/aaa/ContextDagRunnerDemo.java": """package org.example.aaa;

import java.util.*;
import java.util.concurrent.CompletableFuture;
import org.apache.jena.rdf.model.*;
import org.apache.jena.riot.RDFDataMgr;

public class ContextDagRunnerDemo {
    public static void main(String[] args) throws Exception {
        String path = args.length > 0 ? args[0] : "Aaa.ttl";
        Model model = RDFDataMgr.loadModel(path);

        String ns = "http://example.org/Aaa#";
        Resource deviceCls = model.createResource(ns + "Device");
        Resource sensorCls = model.createResource(ns + "Sensor");

        PriorityContextReasoner reasoner = new PriorityContextReasoner(model, 4);

        reasoner.addContext(new PriorityContextReasoner.ContextNode(
            "ctx_devices",
            1,
            Set.of(deviceCls),
            Set.of(),
            List.of(),
            true,
            8
        ));

        reasoner.addContext(new PriorityContextReasoner.ContextNode(
            "ctx_sensors",
            2,
            Set.of(sensorCls),
            Set.of(),
            List.of("ctx_devices"),
            true,
            8
        ));

        Map<String, CompletableFuture<Model>> results = reasoner.runAsync();
        results.forEach((ctxId, fut) -> fut.thenAccept(inferred ->
            System.out.println("Context " + ctxId + " inferred triples: " + inferred.size())
        ));

        CompletableFuture.allOf(results.values().toArray(new CompletableFuture[0])).join();
        reasoner.shutdown();
    }
}
""",

    # ---------------- PYTHON 3 ----------------
    "python/requirements.txt": """rdflib>=7.0.0
""",

    "python/context_reasoner.py": """from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass, field
from typing import Iterable

from rdflib import Graph, RDF, RDFS, OWL, BNode, URIRef
from rdflib.term import Node

RESTRICTION_PROPS = (
    OWL.onProperty,
    OWL.someValuesFrom,
    OWL.allValuesFrom,
    OWL.hasValue,
    OWL.onClass,
)


@dataclass(frozen=True)
class ContextNode:
    context_id: str
    priority: int  # Lower integer = higher priority
    focus_classes: frozenset[URIRef] = frozenset()
    focus_properties: frozenset[URIRef] = frozenset()
    depends_on: tuple[str, ...] = ()
    include_subclasses: bool = True
    max_closure_iterations: int = 8


class FocusedSubgraphExtractor:
    def extract(
        self,
        source: Graph,
        focus_classes: Iterable[URIRef],
        focus_properties: Iterable[URIRef],
        include_subclasses: bool = True,
        max_iterations: int = 8,
    ) -> Graph:
        relevant: set[Node] = set(focus_classes) | set(focus_properties)

        for _ in range(max_iterations):
            newly_added: set[Node] = set()
            for node in relevant:
                if not isinstance(node, (URIRef, BNode)):
                    continue

                newly_added.update(source.objects(node, RDFS.subClassOf))
                newly_added.update(source.objects(node, OWL.equivalentClass))
                newly_added.update(source.subjects(OWL.equivalentClass, node))

                if include_subclasses:
                    newly_added.update(source.subjects(RDFS.subClassOf, node))

                newly_added.update(source.objects(node, RDFS.subPropertyOf))
                newly_added.update(source.objects(node, OWL.equivalentProperty))
                newly_added.update(source.subjects(OWL.equivalentProperty, node))
                newly_added.update(source.objects(node, OWL.inverseOf))
                newly_added.update(source.subjects(OWL.inverseOf, node))
                newly_added.update(source.objects(node, RDFS.domain))
                newly_added.update(source.objects(node, RDFS.range))

                for prop in RESTRICTION_PROPS:
                    for restr in source.subjects(prop, node):
                        newly_added.add(restr)
                        for r_prop in RESTRICTION_PROPS:
                            newly_added.update(source.objects(restr, r_prop))

                for list_prop in (OWL.intersectionOf, OWL.unionOf, RDF.first, RDF.rest):
                    for obj in source.objects(node, list_prop):
                        if obj != RDF.nil:
                            newly_added.add(obj)

            newly_added -= relevant
            if not newly_added:
                break
            relevant |= newly_added

        sub = Graph()
        bnodes_to_copy: set[BNode] = set()

        for s, p, o in source:
            if s in relevant or p in relevant or o in relevant:
                sub.add((s, p, o))
                if isinstance(s, BNode):
                    bnodes_to_copy.add(s)
                if isinstance(o, BNode):
                    bnodes_to_copy.add(o)

        visited_bnodes: set[BNode] = set()
        for bnode in bnodes_to_copy:
            self._copy_bnode_closure(source, bnode, sub, visited_bnodes)

        return sub

    def _copy_bnode_closure(
        self, source: Graph, bnode: BNode, target: Graph, visited: set[BNode]
    ) -> None:
        if bnode in visited:
            return
        visited.add(bnode)
        for _, p, o in source.triples((bnode, None, None)):
            target.add((bnode, p, o))
            if isinstance(o, BNode):
                self._copy_bnode_closure(source, o, target, visited)


class PriorityContextReasoner:
    \"\"\"Priority-aware, DAG-ordered asynchronous context reasoner in Python 3.\"\"\"

    def __init__(self, base_graph: Graph, concurrency: int = 4) -> None:
        self.base_graph = base_graph
        self.concurrency = max(1, concurrency)
        self.extractor = FocusedSubgraphExtractor()
        self.nodes: dict[str, ContextNode] = {}
        self._sem: asyncio.Semaphore | None = None
        self._waiters: list[tuple[int, int, asyncio.Event]] = []

    def add_context(self, node: ContextNode) -> None:
        self.nodes[node.context_id] = node

    def validate_dag(self) -> None:
        in_degree: dict[str, int] = {cid: 0 for cid in self.nodes}
        children: dict[str, list[str]] = {cid: [] for cid in self.nodes}

        for cid, node in self.nodes.items():
            for parent_id in node.depends_on:
                if parent_id not in self.nodes:
                    raise ValueError(f"Unknown parent context '{parent_id}' in '{cid}'")
                in_degree[cid] += 1
                children[parent_id].append(cid)

        queue = deque([cid for cid, deg in in_degree.items() if deg == 0])
        visited = 0
        while queue:
            curr = queue.popleft()
            visited += 1
            for child_id in children[curr]:
                in_degree[child_id] -= 1
                if in_degree[child_id] == 0:
                    queue.append(child_id)

        if visited != len(self.nodes):
            raise ValueError("Cycle detected in context hierarchy DAG.")

    def _reason_context_sync(self, node: ContextNode, parent_inferred: list[Graph]) -> Graph:
        scoped = self.extractor.extract(
            self.base_graph,
            node.focus_classes,
            node.focus_properties,
            include_subclasses=node.include_subclasses,
            max_iterations=node.max_closure_iterations,
        )
        for p_graph in parent_inferred:
            scoped += p_graph

        inferred = Graph()
        subclasses = list(scoped.triples((None, RDFS.subClassOf, None)))
        for c1, _, c2 in subclasses:
            for c2_super in scoped.transitive_objects(c2, RDFS.subClassOf):
                if c1 != c2_super and (c1, RDFS.subClassOf, c2_super) not in scoped:
                    inferred.add((c1, RDFS.subClassOf, c2_super))

        all_classes = set(scoped.subjects(RDFS.subClassOf, None)) | set(
            scoped.objects(RDFS.subClassOf, None)
        )
        for cls in all_classes:
            for sup in scoped.transitive_objects(cls, RDFS.subClassOf):
                for inst in scoped.subjects(RDF.type, cls):
                    if (inst, RDF.type, sup) not in scoped:
                        inferred.add((inst, RDF.type, sup))

        for prop, _, dom in scoped.triples((None, RDFS.domain, None)):
            for subj, _, _ in scoped.triples((None, prop, None)):
                if (subj, RDF.type, dom) not in scoped:
                    inferred.add((subj, RDF.type, dom))

        for prop, _, rng in scoped.triples((None, RDFS.range, None)):
            for _, _, obj in scoped.triples((None, prop, None)):
                if isinstance(obj, (URIRef, BNode)) and (obj, RDF.type, rng) not in scoped:
                    inferred.add((obj, RDF.type, rng))

        return inferred

    async def _run_prioritized(self, priority: int, order: int, coro_factory) -> Graph:
        if self._sem is None:
            self._sem = asyncio.Semaphore(self.concurrency)

        event = asyncio.Event()
        entry = (priority, order, event)
        self._waiters.append(entry)
        self._waiters.sort(key=lambda x: (x[0], x[1]))

        while True:
            is_next = self._waiters[0] is entry
            if is_next and self._sem._value > 0:
                self._waiters.pop(0)
                async with self._sem:
                    if self._waiters:
                        self._waiters[0][2].set()
                    return await coro_factory()
            event.clear()
            try:
                await asyncio.wait_for(event.wait(), timeout=0.01)
            except asyncio.TimeoutError:
                pass

    async def run_async(self) -> dict[str, Graph]:
        self.validate_dag()
        loop = asyncio.get_running_loop()
        results: dict[str, Graph] = {}
        counter = 0

        async def run_with_parents(node: ContextNode) -> Graph:
            nonlocal counter
            parent_graphs: list[Graph] = []
            if node.depends_on:
                parent_graphs = list(
                    await asyncio.gather(*(run_with_parents(self.nodes[pid]) for pid in node.depends_on))
                )

            counter += 1
            order = counter

            async def execute_item() -> Graph:
                return await loop.run_in_executor(
                    None, self._reason_context_sync, node, parent_graphs
                )

            return await self._run_prioritized(node.priority, order, execute_item)

        tasks = {
            cid: asyncio.create_task(run_with_parents(node))
            for cid, node in self.nodes.items()
        }
        for cid, task in tasks.items():
            results[cid] = await task
        return results
""",

    "python/demo.py": """import asyncio
from rdflib import Graph, Namespace, RDFS, OWL, RDF
from context_reasoner import ContextNode, PriorityContextReasoner

AAA = Namespace("http://example.org/Aaa#")


def build_sample_graph() -> Graph:
    g = Graph()
    g.bind("aaa", AAA)
    g.add((AAA.Device, RDF.type, OWL.Class))
    g.add((AAA.Sensor, RDF.type, OWL.Class))
    g.add((AAA.TempSensor, RDF.type, OWL.Class))
    g.add((AAA.Sensor, RDFS.subClassOf, AAA.Device))
    g.add((AAA.TempSensor, RDFS.subClassOf, AAA.Sensor))
    g.add((AAA.tempSensor01, RDF.type, AAA.TempSensor))
    return g


async def main() -> None:
    graph = build_sample_graph()
    reasoner = PriorityContextReasoner(graph, concurrency=4)

    reasoner.add_context(
        ContextNode(
            context_id="ctx_devices",
            priority=1,
            focus_classes=frozenset({AAA.Device}),
            depends_on=(),
        )
    )
    reasoner.add_context(
        ContextNode(
            context_id="ctx_sensors",
            priority=2,
            focus_classes=frozenset({AAA.Sensor}),
            depends_on=("ctx_devices",),
        )
    )

    results = await reasoner.run_async()
    for ctx_id, inferred in results.items():
        print(f"Context '{ctx_id}' inferred {len(inferred)} triples:")
        for s, p, o in inferred:
            print(f"  {s} --{p}--> {o}")


if __name__ == "__main__":
    asyncio.run(main())
""",

    # ---------------- UNREAL ENGINE 5 (C++) PLUGIN ----------------
    "ue5_plugin/ContextReasoner/ContextReasoner.uplugin": """{
  "FileVersion": 3,
  "Version": 1,
  "VersionName": "1.0.0",
  "FriendlyName": "Context Reasoner",
  "Description": "Priority-ordered, DAG-aware focused ontology/context reasoning subsystem for Unreal Engine 5.",
  "Category": "AI",
  "CreatedBy": "Developer",
  "CanContainContent": false,
  "IsBetaVersion": false,
  "Installed": false,
  "Modules": [
    {
      "Name": "ContextReasoner",
      "Type": "Runtime",
      "LoadingPhase": "Default"
    }
  ]
}
""",

    "ue5_plugin/ContextReasoner/Source/ContextReasoner/ContextReasoner.Build.cs": """using UnrealBuildTool;

public class ContextReasoner : ModuleRules
{
    public ContextReasoner(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine"
        });
    }
}
""",

    "ue5_plugin/ContextReasoner/Source/ContextReasoner/Public/ContextReasonerTypes.h": """#pragma once

#include "CoreMinimal.h"
#include "ContextReasonerTypes.generated.h"

USTRUCT(BlueprintType)
struct CONTEXTREASONER_API FOntologyTriple
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    FString Subject;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    FString Predicate;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    FString Object;

    bool operator==(const FOntologyTriple& Other) const
    {
        return Subject == Other.Subject && Predicate == Other.Predicate && Object == Other.Object;
    }
};

FORCEINLINE uint32 GetTypeHash(const FOntologyTriple& Triple)
{
    uint32 Hash = GetTypeHash(Triple.Subject);
    Hash = HashCombine(Hash, GetTypeHash(Triple.Predicate));
    Hash = HashCombine(Hash, GetTypeHash(Triple.Object));
    return Hash;
}

USTRUCT(BlueprintType)
struct CONTEXTREASONER_API FReasoningContextNode
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    FName ContextId;

    /** Lower integer means higher scheduling priority. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    int32 Priority = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    TSet<FString> FocusClasses;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    TSet<FString> FocusProperties;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    TArray<FName> DependsOn;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    bool bIncludeSubClasses = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ContextReasoner")
    int32 MaxClosureIterations = 8;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(
    FOnContextReasoningComplete,
    FName, ContextId,
    int32, InferredTripleCount
);
""",

    "ue5_plugin/ContextReasoner/Source/ContextReasoner/Public/ContextReasonerSubsystem.h": """#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "ContextReasonerTypes.h"
#include "ContextReasonerSubsystem.generated.h"

/**
 * GameInstanceSubsystem that orchestrates priority-ordered, DAG-aware focused
 * ontology/context reasoning asynchronously on UE5 worker threads and notifies
 * the Game Thread upon completion.
 */
UCLASS()
class CONTEXTREASONER_API UContextReasonerSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    UFUNCTION(BlueprintCallable, Category = "ContextReasoner")
    void LoadBaseTriples(const TArray<FOntologyTriple>& Triples);

    UFUNCTION(BlueprintCallable, Category = "ContextReasoner")
    void RegisterContext(const FReasoningContextNode& Node);

    UFUNCTION(BlueprintCallable, Category = "ContextReasoner")
    bool ValidateContextDag(FString& OutError) const;

    /** Starts priority-ordered DAG reasoning across registered contexts. */
    UFUNCTION(BlueprintCallable, Category = "ContextReasoner")
    void StartPriorityReasoningAsync();

    UFUNCTION(BlueprintCallable, Category = "ContextReasoner")
    TArray<FOntologyTriple> GetInferredTriplesForContext(FName ContextId) const;

    UPROPERTY(BlueprintAssignable, Category = "ContextReasoner")
    FOnContextReasoningComplete OnContextReasoningComplete;

private:
    void ExtractFocusedSubgraph(
        const FReasoningContextNode& Node,
        TSet<FOntologyTriple>& OutScopedTriples) const;

    TArray<FOntologyTriple> RunContextInference(
        const FReasoningContextNode& Node,
        const TArray<FOntologyTriple>& ParentInferred) const;

    void ScheduleReadyContexts();

    TArray<FOntologyTriple> BaseTriples;
    TMap<FName, FReasoningContextNode> ContextNodes;
    TMap<FName, TArray<FOntologyTriple>> InferredByContext;
    TSet<FName> CompletedContexts;
    TSet<FName> ScheduledContexts;
    mutable FCriticalSection StateMutex;
};
""",

    "ue5_plugin/ContextReasoner/Source/ContextReasoner/Private/ContextReasonerSubsystem.cpp": """#include "ContextReasonerSubsystem.h"
#include "Async/Async.h"

namespace OntologyUri
{
    static const FString RdfsSubClassOf = TEXT("http://www.w3.org/2000/01/rdf-schema#subClassOf");
    static const FString RdfsSubPropertyOf = TEXT("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
    static const FString RdfsDomain = TEXT("http://www.w3.org/2000/01/rdf-schema#domain");
    static const FString RdfsRange = TEXT("http://www.w3.org/2000/01/rdf-schema#range");
    static const FString RdfType = TEXT("http://www.w3.org/1999/02/22-rdf-syntax-ns#type");
}

void UContextReasonerSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
}

void UContextReasonerSubsystem::Deinitialize()
{
    FScopeLock Lock(&StateMutex);
    BaseTriples.Empty();
    ContextNodes.Empty();
    InferredByContext.Empty();
    CompletedContexts.Empty();
    ScheduledContexts.Empty();
    Super::Deinitialize();
}

void UContextReasonerSubsystem::LoadBaseTriples(const TArray<FOntologyTriple>& Triples)
{
    FScopeLock Lock(&StateMutex);
    BaseTriples = Triples;
}

void UContextReasonerSubsystem::RegisterContext(const FReasoningContextNode& Node)
{
    FScopeLock Lock(&StateMutex);
    ContextNodes.Add(Node.ContextId, Node);
}

bool UContextReasonerSubsystem::ValidateContextDag(FString& OutError) const
{
    FScopeLock Lock(&StateMutex);

    TMap<FName, int32> InDegree;
    TMap<FName, TArray<FName>> Children;

    for (const auto& Pair : ContextNodes)
    {
        InDegree.Add(Pair.Key, 0);
        Children.Add(Pair.Key, {});
    }

    for (const auto& Pair : ContextNodes)
    {
        const FReasoningContextNode& Node = Pair.Value;
        for (const FName& ParentId : Node.DependsOn)
        {
            if (!ContextNodes.Contains(ParentId))
            {
                OutError = FString::Printf(
                    TEXT("Context '%s' depends on unknown parent '%s'."),
                    *Node.ContextId.ToString(),
                    *ParentId.ToString()
                );
                return false;
            }
            InDegree[Node.ContextId]++;
            Children[ParentId].Add(Node.ContextId);
        }
    }

    TArray<FName> ReadyQueue;
    for (const auto& Pair : InDegree)
    {
        if (Pair.Value == 0)
        {
            ReadyQueue.Add(Pair.Key);
        }
    }

    int32 Visited = 0;
    while (ReadyQueue.Num() > 0)
    {
        const FName Current = ReadyQueue[0];
        ReadyQueue.RemoveAt(0);
        Visited++;

        for (const FName& ChildId : Children[Current])
        {
            InDegree[ChildId]--;
            if (InDegree[ChildId] == 0)
            {
                ReadyQueue.Add(ChildId);
            }
        }
    }

    if (Visited != ContextNodes.Num())
    {
        OutError = TEXT("Cycle detected in reasoning context DAG.");
        return false;
    }

    OutError.Empty();
    return true;
}

void UContextReasonerSubsystem::StartPriorityReasoningAsync()
{
    FString ErrorMsg;
    if (!ValidateContextDag(ErrorMsg))
    {
        UE_LOG(LogTemp, Error, TEXT("ContextReasoner DAG invalid: %s"), *ErrorMsg);
        return;
    }

    {
        FScopeLock Lock(&StateMutex);
        InferredByContext.Empty();
        CompletedContexts.Empty();
        ScheduledContexts.Empty();
    }

    ScheduleReadyContexts();
}

void UContextReasonerSubsystem::ScheduleReadyContexts()
{
    TArray<FReasoningContextNode> ReadyNodes;

    {
        FScopeLock Lock(&StateMutex);
        for (const auto& Pair : ContextNodes)
        {
            const FName& ContextId = Pair.Key;
            const FReasoningContextNode& Node = Pair.Value;

            if (ScheduledContexts.Contains(ContextId) || CompletedContexts.Contains(ContextId))
            {
                continue;
            }

            bool bParentsDone = true;
            for (const FName& ParentId : Node.DependsOn)
            {
                if (!CompletedContexts.Contains(ParentId))
                {
                    bParentsDone = false;
                    break;
                }
            }

            if (bParentsDone)
            {
                ReadyNodes.Add(Node);
            }
        }

        ReadyNodes.Sort([](const FReasoningContextNode& A, const FReasoningContextNode& B)
        {
            return A.Priority < B.Priority;
        });

        for (const FReasoningContextNode& Node : ReadyNodes)
        {
            ScheduledContexts.Add(Node.ContextId);
        }
    }

    for (const FReasoningContextNode& Node : ReadyNodes)
    {
        TArray<FOntologyTriple> CombinedParentTriples;
        {
            FScopeLock Lock(&StateMutex);
            for (const FName& ParentId : Node.DependsOn)
            {
                if (const TArray<FOntologyTriple>* ParentOut = InferredByContext.Find(ParentId))
                {
                    CombinedParentTriples.Append(*ParentOut);
                }
            }
        }

        const FName ContextId = Node.ContextId;
        TWeakObjectPtr<UContextReasonerSubsystem> WeakThis(this);

        AsyncTask(ENamedThreads::AnyBackgroundThreadNormalTask,
            [WeakThis, Node, CombinedParentTriples]()
            {
                UContextReasonerSubsystem* StrongThis = WeakThis.Get();
                if (!StrongThis)
                {
                    return;
                }

                TArray<FOntologyTriple> Inferred = StrongThis->RunContextInference(Node, CombinedParentTriples);
                const int32 Count = Inferred.Num();

                AsyncTask(ENamedThreads::GameThread,
                    [WeakThis, ContextId, Inferred = MoveTemp(Inferred), Count]()
                    {
                        UContextReasonerSubsystem* GameThreadThis = WeakThis.Get();
                        if (!GameThreadThis)
                        {
                            return;
                        }

                        {
                            FScopeLock Lock(&GameThreadThis->StateMutex);
                            GameThreadThis->InferredByContext.Add(ContextId, Inferred);
                            GameThreadThis->CompletedContexts.Add(ContextId);
                        }

                        GameThreadThis->OnContextReasoningComplete.Broadcast(ContextId, Count);
                        GameThreadThis->ScheduleReadyContexts();
                    });
            });
    }
}

void UContextReasonerSubsystem::ExtractFocusedSubgraph(
    const FReasoningContextNode& Node,
    TSet<FOntologyTriple>& OutScopedTriples) const
{
    TSet<FString> RelevantEntities;
    RelevantEntities.Append(Node.FocusClasses);
    RelevantEntities.Append(Node.FocusProperties);

    for (int32 Iter = 0; Iter < Node.MaxClosureIterations; ++Iter)
    {
        TSet<FString> NewlyAdded;
        for (const FOntologyTriple& T : BaseTriples)
        {
            if (T.Predicate == OntologyUri::RdfsSubClassOf)
            {
                if (RelevantEntities.Contains(T.Subject))
                {
                    NewlyAdded.Add(T.Object);
                }
                if (Node.bIncludeSubClasses && RelevantEntities.Contains(T.Object))
                {
                    NewlyAdded.Add(T.Subject);
                }
            }
            else if (T.Predicate == OntologyUri::RdfsSubPropertyOf)
            {
                if (RelevantEntities.Contains(T.Subject))
                {
                    NewlyAdded.Add(T.Object);
                }
            }
            else if (T.Predicate == OntologyUri::RdfsDomain || T.Predicate == OntologyUri::RdfsRange)
            {
                if (RelevantEntities.Contains(T.Subject))
                {
                    NewlyAdded.Add(T.Object);
                }
            }
        }

        NewlyAdded = NewlyAdded.Difference(RelevantEntities);
        if (NewlyAdded.Num() == 0)
        {
            break;
        }
        RelevantEntities.Append(NewlyAdded);
    }

    OutScopedTriples.Reset();
    for (const FOntologyTriple& T : BaseTriples)
    {
        if (RelevantEntities.Contains(T.Subject) ||
            RelevantEntities.Contains(T.Predicate) ||
            RelevantEntities.Contains(T.Object))
        {
            OutScopedTriples.Add(T);
        }
    }
}

TArray<FOntologyTriple> UContextReasonerSubsystem::RunContextInference(
    const FReasoningContextNode& Node,
    const TArray<FOntologyTriple>& ParentInferred) const
{
    TSet<FOntologyTriple> ScopedSet;
    ExtractFocusedSubgraph(Node, ScopedSet);
    for (const FOntologyTriple& PT : ParentInferred)
    {
        ScopedSet.Add(PT);
    }

    TSet<FOntologyTriple> InferredSet;

    for (const FOntologyTriple& T1 : ScopedSet)
    {
        if (T1.Predicate != OntologyUri::RdfsSubClassOf)
        {
            continue;
        }
        for (const FOntologyTriple& T2 : ScopedSet)
        {
            if (T2.Predicate == OntologyUri::RdfsSubClassOf && T1.Object == T2.Subject)
            {
                FOntologyTriple Transitive{T1.Subject, OntologyUri::RdfsSubClassOf, T2.Object};
                if (!ScopedSet.Contains(Transitive))
                {
                    InferredSet.Add(Transitive);
                }
            }
        }
    }

    for (const FOntologyTriple& TypeTriple : ScopedSet)
    {
        if (TypeTriple.Predicate != OntologyUri::RdfType)
        {
            continue;
        }
        for (const FOntologyTriple& SubTriple : ScopedSet)
        {
            if (SubTriple.Predicate == OntologyUri::RdfsSubClassOf && SubTriple.Subject == TypeTriple.Object)
            {
                FOntologyTriple InferredType{TypeTriple.Subject, OntologyUri::RdfType, SubTriple.Object};
                if (!ScopedSet.Contains(InferredType))
                {
                    InferredSet.Add(InferredType);
                }
            }
        }
    }

    return InferredSet.Array();
}

TArray<FOntologyTriple> UContextReasonerSubsystem::GetInferredTriplesForContext(FName ContextId) const
{
    FScopeLock Lock(&StateMutex);
    if (const TArray<FOntologyTriple>* Found = InferredByContext.Find(ContextId))
    {
        return *Found;
    }
    return {};
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

zip_path = "/tmp/hierarchical-context-reasoner-java-py3-ue5.zip"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for root, _, filenames in os.walk(base_dir):
        for fn in sorted(filenames):
            abs_p = os.path.join(root, fn)
            arc_p = os.path.relpath(abs_p, base_dir)
            zf.write(abs_p, arc_p)

print("Created zip:", zip_path, "Size:", os.path.getsize(zip_path))
with zipfile.ZipFile(zip_path, "r") as zf:
    for info in zf.infolist():
        print(" -", info.filename, info.file_size)