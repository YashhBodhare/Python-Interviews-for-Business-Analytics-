# 🛡️ Technical review and version notes

[← Study hub](README.md)

The guide rewrites the supplied topic coverage in accessible language and adds original business examples. Version-sensitive statements were checked against official documentation in October 2026. The Python examples target 3.11+ and were executed on **Python 3.12.14**; the pandas business lab ran with **pandas 2.2.3**.

## Corrections worth remembering

| Topic | Accurate interpretation | Official reference |
|---|---|---|
| Identity | is checks identity and has legitimate sentinel/identity uses beyond None. Value equality does not imply identity. | [Data model](https://docs.python.org/3/reference/datamodel.html) |
| Interning | Literal reuse can occur outside the small-integer cache. Do not promise that 257 always produces different objects. | [Objects and identity](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types) |
| Mutable values inside tuples | A tuple cannot replace its members, but a mutable member can change. | [Built-in types](https://docs.python.org/3/library/stdtypes.html) |
| Dataclass freezing | Frozen blocks ordinary reassignment, not nested mutation. Generated hashing still requires hashable participating fields. | [Dataclasses](https://docs.python.org/3/library/dataclasses.html) |
| Equality and hashing | Defining equality does not mean every class must add hashing; leaving a mutable value class unhashable can be appropriate. | [Hash contract](https://docs.python.org/3/reference/datamodel.html#object.__hash__) |
| Generator memory | Lazy output avoids storing all results, but sources and intermediates still use memory. | [Expressions](https://docs.python.org/3/reference/expressions.html#generator-expressions) |
| zip strict | Detects mismatched lengths; does not rewind or preserve already consumed inputs. | [zip](https://docs.python.org/3/library/functions.html#zip) |
| groupby | Groups consecutive equal keys. Sort by the same key when global grouping is needed; advancing the iterator invalidates prior shared groups. | [itertools](https://docs.python.org/3/library/itertools.html#itertools.groupby) |
| EAFP | Exception handling does not automatically make an operation atomic or race-free. | [Glossary](https://docs.python.org/3/glossary.html#term-EAFP) |
| Protocols and ABCs | Protocol hints describe structure; limited runtime checks do not validate full signatures. ABC recognition can include virtual registration. | [Typing](https://docs.python.org/3/library/typing.html#typing.Protocol), [abc](https://docs.python.org/3/library/abc.html) |
| functools.wraps | Preserves selected metadata and provides __wrapped__; does not erase wrapper behaviour. | [functools](https://docs.python.org/3/library/functools.html#functools.wraps) |
| Caching | Can be stale or unbounded; concurrent first calls may execute the function more than once. | [Caching](https://docs.python.org/3/library/functools.html#functools.lru_cache) |
| Task groups and deadlines | Cancellation is cooperative. TaskGroup normally cancels siblings on non-cancellation failure; gather has a different default failure policy. External effects are not rolled back. | [Async tasks](https://docs.python.org/3/library/asyncio-task.html) |
| GIL and locks | Do not infer safety of a compound update from the GIL or a fixed bytecode count. Match the synchronisation mechanism to the shared resource. | [Threading](https://docs.python.org/3/library/threading.html) |
| Free-threaded Python | Experimental optional build in 3.13; officially supported and optional in 3.14. Scaling and extension compatibility must be measured. | [PEP 779](https://peps.python.org/pep-0779/), [Free threading](https://docs.python.org/3/howto/free-threading-python.html) |
| pandas merge | Missing keys can match each other. m:m validation does not enforce uniqueness. | [merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) |
| pandas Copy-on-Write | Default and only mode in 3.0; optional in 2.x. Use explicit .loc assignment. | [Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html) |
| Performance claims | Vectorisation and built-in aggregation are useful candidates, not universal fixed-factor speedups. | [pandas performance](https://pandas.pydata.org/docs/user_guide/enhancingperf.html) |

## Limits of the checks

All 50 standalone interview examples passed. The business lab passed eight result checks, and all 12 Python code blocks in the cheat sheet executed successfully in sequence. The pack's internal links, unique question IDs and one-scenario-per-question coverage were checked separately.

The checks do not establish production readiness, validate every platform or package version, run a static type checker, or benchmark multiprocessing or free-threaded performance. Configuration-inspection examples demonstrate inspection only. Where operational engineering is involved, the BA defines requirements and acceptance criteria and works with the authorised implementation owner.
