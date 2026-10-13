import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

import generate_catalog as gen


def node(artifact, scope="compile", children=None, group="org.example", version="1.0", kind="jar", classifier=""):
    result = {"groupId": group, "artifactId": artifact, "version": version, "type": kind,
              "scope": scope, "classifier": classifier, "optional": "false"}
    if children is not None:
        result["children"] = children
    return result


def tree(*children):
    root = node("java-demo", scope="", group="nl.kadaster.demo", version="1.0.0-SNAPSHOT")
    root["children"] = list(children)
    return root


def documents(text):
    body = "".join(line for line in text.splitlines(True) if not line.startswith("#"))
    return [json.loads(doc) for doc in body.split("\n---\n") if doc.strip()]


def entities(tree_data):
    files = gen.render(tree_data)
    return documents(files[gen.DEPENDENCIES_FILE])[0], {
        e["metadata"]["title"]: e for e in documents(files[gen.LIBRARIES_FILE])}


class GenerateCatalogTest(unittest.TestCase):
    def test_direct_and_transitive_edges_with_scopes(self):
        direct, libs = entities(tree(node("api", children=[node("core")]), node("junit", "test", [node("hamcrest", "test")])))
        api, core, junit = (libs[f"org.example:{a}:1.0"] for a in ("api", "core", "junit"))
        self.assertEqual(direct, sorted(gen.COMPONENT_PREFIX + e["metadata"]["name"] for e in (api, junit)))
        self.assertEqual(api["spec"]["dependsOn"], [gen.COMPONENT_PREFIX + core["metadata"]["name"]])
        self.assertNotIn("dependsOn", core["spec"])
        self.assertEqual(junit["metadata"]["annotations"]["maven.apache.org/scopes"], "test")
        self.assertIn("maven-scope-test", junit["metadata"]["tags"])
        self.assertIn("Test-only", junit["metadata"]["description"])
        self.assertIn("maven-scope-test", libs["org.example:hamcrest:1.0"]["metadata"]["tags"])
        self.assertNotIn("Test-only", api["metadata"]["description"])
        self.assertEqual(api["spec"]["type"], "library")
        self.assertEqual(api["spec"]["owner"], gen.OWNER)
        self.assertEqual(len(libs), 4)

    def test_shared_node_merges_scopes_and_edges(self):
        _, libs = entities(tree(node("a", children=[node("shared", children=[node("x")])]),
                                node("b", "test", [node("shared", "test", [node("y", "test")])])))
        shared = libs["org.example:shared:1.0"]
        self.assertEqual(shared["metadata"]["annotations"]["maven.apache.org/scopes"], "compile,test")
        self.assertEqual(shared["metadata"]["tags"], ["java", "maven", "maven-scope-compile", "maven-scope-test"])
        self.assertNotIn("Test-only", shared["metadata"]["description"])
        self.assertEqual(len(shared["spec"]["dependsOn"]), 2)
        self.assertEqual(len(libs), 5)

    def test_coordinate_identity_includes_version_type_and_classifier(self):
        _, libs = entities(tree(node("lib"), node("lib", version="2.0"), node("lib", classifier="tests"),
                                node("lib", kind="test-jar", classifier="tests")))
        self.assertEqual(sorted(libs), ["org.example:lib:1.0", "org.example:lib:2.0",
                                        "org.example:lib:jar:tests:1.0", "org.example:lib:test-jar:tests:1.0"])
        names = [e["metadata"]["name"] for e in libs.values()]
        self.assertEqual(len(set(names)), 4)

    def test_names_are_stable_and_bounded(self):
        identity = ("org.example", "A" * 100 + ".Lib", "1.0", "jar", "")
        name = gen.entity_name(identity)
        self.assertEqual(name, gen.entity_name(identity))
        self.assertLessEqual(len(name), 63)
        self.assertRegex(name, r"^maven-a+-[0-9a-f]{12}$")

    def test_output_is_deterministic_regardless_of_child_order(self):
        first = gen.render(tree(node("a", children=[node("c"), node("b")]), node("d")))
        second = gen.render(tree(node("d"), node("a", children=[node("b"), node("c")])))
        self.assertEqual(first, second)

    def test_empty_dependencies(self):
        files = gen.render(tree())
        self.assertEqual(documents(files[gen.DEPENDENCIES_FILE]), [[]])
        self.assertEqual(documents(files[gen.LIBRARIES_FILE]), [])
        files = gen.render({k: v for k, v in tree().items() if k != "children"})
        self.assertEqual(documents(files[gen.LIBRARIES_FILE]), [])

    def test_invalid_input(self):
        valid = tree(node("a", children=[node("b")]))
        cases = {
            "wrong root": lambda t: t.update(artifactId="other"),
            "scoped root": lambda t: t.update(scope="compile"),
            "not an object": lambda t: t["children"].append([]),
            "missing key": lambda t: t["children"][0].pop("version"),
            "unknown key": lambda t: t["children"][0].update(extra="x"),
            "non-string": lambda t: t["children"][0].update(version=1),
            "bad coordinate": lambda t: t["children"][0].update(groupId="org example"),
            "empty version": lambda t: t["children"][0].update(version=""),
            "bad classifier": lambda t: t["children"][0].update(classifier="a:b"),
            "unsupported scope": lambda t: t["children"][0].update(scope="import"),
            "empty scope": lambda t: t["children"][0]["children"][0].update(scope=""),
            "bad optional": lambda t: t["children"][0].update(optional=False),
            "children type": lambda t: t["children"][0].update(children={}),
            "self dependency": lambda t: t["children"][0]["children"].append(node("a")),
            "root dependency": lambda t: t["children"].append(
                node("java-demo", group="nl.kadaster.demo", version="1.0.0-SNAPSHOT")),
        }
        for label, mutate in cases.items():
            with self.subTest(label):
                broken = copy.deepcopy(valid)
                mutate(broken)
                with self.assertRaises(gen.TreeError):
                    gen.render(broken)
        with self.assertRaises(gen.TreeError):
            gen.render([])

    def test_check_detects_stale_output_without_writing(self):
        files = gen.render(tree(node("a")))
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.assertEqual(gen.sync(files, directory, check=True), sorted(files))
            self.assertEqual(list(directory.iterdir()), [])
            self.assertEqual(gen.sync(files, directory, check=False), sorted(files))
            self.assertEqual(gen.sync(files, directory, check=True), [])
            (directory / gen.LIBRARIES_FILE).write_text("stale", encoding="utf-8")
            self.assertEqual(gen.sync(files, directory, check=True), [gen.LIBRARIES_FILE])

    def test_cli_check_and_invalid_tree_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            stale = Path(tmp) / "tree.json"
            stale.write_text(json.dumps(tree(node("not-resolved-for-java-demo"))), encoding="utf-8")
            invalid = Path(tmp) / "invalid.json"
            invalid.write_text("{", encoding="utf-8")
            with redirect_stderr(io.StringIO()) as err:
                self.assertEqual(gen.main(["--check", "--dependency-tree", str(stale)]), 1)
                self.assertEqual(gen.main(["--check", "--dependency-tree", str(invalid)]), 2)
            self.assertIn("stale generated files", err.getvalue())


if __name__ == "__main__":
    unittest.main()
