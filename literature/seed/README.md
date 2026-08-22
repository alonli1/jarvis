# Jarvis Physics Seed Corpus — 2026-08-21

This is a curated **seed corpus**, not an exhaustive literature dump. It is optimized for retrieval around EFT matching, gravity, inverse UV reconstruction, and automated theoretical-physics tools.

## Ingestion policy

- **T0 — Core:** ingest first and give high retrieval authority.
- **T1 — Important:** ingest after T0.
- **T2 — Background/tooling:** ingest selectively or retain metadata for discovery.
- For arXiv works, use the official arXiv copy.
- For commercial books/paywalled papers, keep metadata until the group supplies a lawful institutional/personal copy.

The manifest contains **75 references**, of which **34 are T0 core sources**.

## Foundations of EFT

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T0 | [**Infrared Singularities and Massive Fields** — Thomas Appelquist, J. Carazzone (1975); DOI:10.1103/PhysRevD.11.2856](https://doi.org/10.1103/PhysRevD.11.2856) | Foundational decoupling theorem underlying heavy-field EFT matching. | `metadata_and_abstract_unless_licensed` |
| T0 | [**Phenomenological Lagrangians** — Steven Weinberg (1979); DOI:10.1016/0378-4371(79)90223-1](https://doi.org/10.1016/0378-4371(79)90223-1) | Classic statement of the modern EFT viewpoint. | `metadata_and_abstract_unless_licensed` |
| T1 | [**Effective Field Theory, Past and Future** — Steven Weinberg (2009); arXiv:0908.1964](https://arxiv.org/abs/0908.1964) | Compact conceptual review of the EFT philosophy. | `download_arxiv` |
| T0 | [**Introduction to Effective Field Theories** — Aneesh V. Manohar (2018); arXiv:1804.05863](https://arxiv.org/abs/1804.05863) | Modern pedagogical EFT reference covering matching, running and power counting. | `download_arxiv` |
| T0 | [**Introduction to Effective Field Theory** — C. P. Burgess (2020); DOI:10.1017/9781139048040](https://www.cambridge.org/core/books/introduction-to-effective-field-theory/A9CDB35F4AA7921E3A9CFD573EBA8B64) | Broad systematic EFT textbook; excellent canonical background source. | `metadata_only_until_licensed_copy` |

## Automated and one-loop EFT matching

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T1 | [**How to use the Standard Model effective field theory** — Brian Henning, Xiaochuan Lu, Hitoshi Murayama (2014); arXiv:1412.1837](https://arxiv.org/abs/1412.1837) | Important bridge between functional methods, CDE and practical EFT matching. | `download_arxiv` |
| T0 | [**One-loop Matching and Running with Covariant Derivative Expansion** — Brian Henning, Xiaochuan Lu, Hitoshi Murayama (2016); arXiv:1604.01019](https://arxiv.org/abs/1604.01019) | Core functional one-loop matching/CDE reference. | `download_arxiv` |
| T0 | [**The Universal One-Loop Effective Action** — Aleksandra Drozd, John Ellis, Jérémie Quevillon, Tevong You (2015); arXiv:1512.03003](https://arxiv.org/abs/1512.03003) | Foundational universal formulae for one-loop matching. | `download_arxiv` |
| T0 | [**The Fermionic Universal One-Loop Effective Action** — John Ellis, Jérémie Quevillon, Théo Vuong, Tevong You, Zhengkang Zhang (2020); arXiv:2006.16260](https://arxiv.org/abs/2006.16260) | Universal one-loop structures involving heavy fermions; directly useful for heavy-fermion gravity matching. | `download_arxiv` |
| T0 | [**Functional Prescription for Effective Field Theory Matching** — Timothy Cohen, Xiaochuan Lu, Zhengkang Zhang (2020); arXiv:2011.02484](https://arxiv.org/abs/2011.02484) | Systematic functional prescription separating hard and soft contributions. | `download_arxiv` |
| T0 | [**SuperTracer: A Calculator of Functional Supertraces for One-Loop EFT Matching** — Javier Fuentes-Martín, Matthias König, Julie Pagès, Anders Eller Thomsen, Felix Wilsch (2020); arXiv:2012.08506](https://arxiv.org/abs/2012.08506) | Direct precursor to automated functional matching workflows. | `download_arxiv` |
| T1 | [**STrEAMlining EFT Matching** — Timothy Cohen, Xiaochuan Lu, Zhengkang Zhang (2020); arXiv:2012.07851](https://arxiv.org/abs/2012.07851) | Independent automation of supertrace-based one-loop matching. | `download_arxiv` |
| T0 | [**Matchmakereft: automated tree-level and one-loop matching** — Adrian Carmona, Achilleas Lazopoulos, Pablo Olgoso, Jose Santiago (2021); arXiv:2112.10787](https://arxiv.org/abs/2112.10787) | Major general automated matching system; essential comparison point. | `download_arxiv` |
| T0 | [**A Proof of Concept for Matchete: An Automated Tool for Matching Effective Theories** — Javier Fuentes-Martín, Matthias König, Julie Pagès, Anders Eller Thomsen, Felix Wilsch (2022); arXiv:2212.04510](https://arxiv.org/abs/2212.04510) | Central automated functional matching tool and key infrastructure for the planned gravity work. | `download_arxiv` |
| T1 | [**CoDEx: Wilson coefficient calculator connecting SMEFT to UV theory** — Subhadip Das Bakshi, Joydeep Chakrabortty, Sunando Kumar Patra (2018); arXiv:1808.04403](https://arxiv.org/abs/1808.04403) | Earlier automated Wilson-coefficient/matching framework. | `download_arxiv` |
| T1 | [**MatchingTools: a Python library for symbolic effective field theory calculations** — Juan C. Criado (2017); arXiv:1710.06445](https://arxiv.org/abs/1710.06445) | Useful earlier symbolic matching architecture. | `download_arxiv` |
| T1 | [**An Efficient On-shell Framework for EFT Matching** — Ziyu Dong, Cihang Li, Teng Ma, Jing Shu, Zizheng Zhou (2025); arXiv:2507.17829](https://arxiv.org/abs/2507.17829) | Current on-shell alternative to functional/diagrammatic matching, designed with automation in mind. | `download_arxiv` |
| T1 | [**SUSY meets SMEFT: Complete one-loop matching of the general MSSM** — Sabine Kraml, Andre Lessa, Suraj Prakash, Felix Wilsch (2025); arXiv:2506.05201](https://arxiv.org/abs/2506.05201) | Large real-world stress test of Matchete and evidence for scaling automated matching. | `download_arxiv` |
| T1 | [**Matchotter: An Automated Tool for Dimensional Reduction at Finite Temperature** — Javier Fuentes-Martín, Javier López Miras, Adrián Moreno-Sánchez (2026); arXiv:2604.21972](https://arxiv.org/abs/2604.21972) | Shows 2026 expansion of the Matchete ecosystem into another matching domain. | `download_arxiv` |
| T1 | [**Effective Lagrangians from functional matching** — Stefan Dittmaier, Sebastian Schuhmacher, Maximilian Stahlhofen (2026); arXiv:2608.11306](https://arxiv.org/abs/2608.11306) | Very recent functional-matching treatment; keeps the corpus current as of 2026-08-21. | `download_arxiv` |

## Inverse UV/IR dictionaries and UV reconstruction

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T0 | [**Effective description of general extensions of the Standard Model: the complete tree-level dictionary** — J. de Blas, J. C. Criado, M. Pérez-Victoria, J. Santiago (2017); arXiv:1711.10391](https://arxiv.org/abs/1711.10391) | Direct precedent for systematic mapping from low-energy EFT operators to broad classes of UV completions. | `download_arxiv` |
| T0 | [**Towards the one loop IR/UV dictionary in the SMEFT: one loop generated operators from new scalars and fermions** — Guilherme Guedes, Pablo Olgoso, Jose Santiago (2023); arXiv:2303.16965](https://arxiv.org/abs/2303.16965) | Introduces SOLD and explicitly targets one-loop IR/UV dictionaries. | `download_arxiv` |
| T0 | [**From the EFT to the UV: the complete SMEFT one-loop dictionary** — Guilherme Guedes, Pablo Olgoso (2024); arXiv:2412.14253; DOI:10.21468/SciPostPhys.20.3.074](https://arxiv.org/abs/2412.14253) | Closest current precedent to automated inverse UV reconstruction; published in SciPost Physics in 2026. | `download_arxiv` |
| T1 | [**A complete tree-level dictionary between simplified BSM models and SMEFT (d≤7) operators** — Hao-Lin Li, Yu-Hang Ni, Ming-Lei Xiao, Jiang-Hao Yu (2023); arXiv:2307.10380](https://arxiv.org/abs/2307.10380) | Extends systematic UV/EFT dictionaries to higher operator dimension. | `download_arxiv` |
| T0 | [**Field redefinitions in effective theories at higher orders** — Juan Carlos Criado, Manuel Pérez-Victoria (2018); arXiv:1811.09413](https://arxiv.org/abs/1811.09413) | Essential for inverse matching that must quotient physically redundant descriptions. | `download_arxiv` |

## Gravity EFT, curved spacetime and heat kernels

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T0 | [**General relativity as an effective field theory: The leading quantum corrections** — John F. Donoghue (1994); arXiv:gr-qc/9405057](https://arxiv.org/abs/gr-qc/9405057) | Canonical starting point for GR as a low-energy quantum EFT. | `download_arxiv` |
| T1 | [**Introduction to the Effective Field Theory Description of Gravity** — John F. Donoghue (1995); arXiv:gr-qc/9512024](https://arxiv.org/abs/gr-qc/9512024) | Pedagogical presentation of the gravitational EFT viewpoint. | `download_arxiv` |
| T0 | [**Quantum Gravity in Everyday Life: General Relativity as an Effective Field Theory** — C. P. Burgess (2003); arXiv:gr-qc/0311082](https://arxiv.org/abs/gr-qc/0311082) | Clear review of gravity as an EFT and power counting. | `download_arxiv` |
| T1 | [**Quantum General Relativity and Effective Field Theory** — John F. Donoghue (2022); arXiv:2211.09902](https://arxiv.org/abs/2211.09902) | Modern status review of quantum GR as an EFT. | `download_arxiv` |
| T0 | [**Effective Field Theory of Gravity to All Orders** — Marvin Ruhdorfer, Javi Serra, Andreas Weiler (2019); arXiv:1908.08050](https://arxiv.org/abs/1908.08050) | Systematic gravitational EFT operator classification; important for arbitrary-order gravity EFT targets. | `download_arxiv` |
| T0 | [**Covariant derivative expansion for the renormalization of gravity** — Rodrigo Alonso (2019); arXiv:1912.09671](https://arxiv.org/abs/1912.09671) | Direct bridge between CDE methods and gravitational renormalization. | `download_arxiv` |
| T0 | [**The Universal One-Loop Effective Action with Gravity** — Sophie Larue, Jérémie Quevillon (2023); arXiv:2303.10203](https://arxiv.org/abs/2303.10203) | One of the most directly relevant papers for automated one-loop matching with gravity. | `download_arxiv` |
| T1 | [**The Geometric Universal One-Loop Effective Action** — Xu-Xiang Li, Xiaochuan Lu, Zhengkang Zhang (2024); arXiv:2411.04173](https://arxiv.org/abs/2411.04173) | Geometric formulation of one-loop matching and field redefinitions; useful for nonlinear field-space structures. | `download_arxiv` |
| T0 | [**Heat kernel expansion: user's manual** — D. V. Vassilevich (2003); arXiv:hep-th/0306138](https://arxiv.org/abs/hep-th/0306138) | Canonical practical reference for heat-kernel coefficients and one-loop effective actions. | `download_arxiv` |
| T1 | [**Top-down approach to the curved spacetime effective field theory** — Łukasz Nakonieczny (2020); arXiv:2004.12320](https://arxiv.org/abs/2004.12320) | Explicit top-down curved-spacetime EFT perspective with examples. | `download_arxiv` |
| T0 | [**Covariant derivative of fermions and all that** — Ilya L. Shapiro (2016); arXiv:1611.02263](https://arxiv.org/abs/1611.02263) | Useful for curved-spacetime fermions and conventions needed for graviton–fermion vertices. | `download_arxiv` |
| T0 | [**Gravity-Matter Feynman Rules for any Valence** — David Prinz (2020); arXiv:2004.09543](https://arxiv.org/abs/2004.09543) | Directly useful for higher graviton–matter vertices and automated gravity matching. | `download_arxiv` |
| T1 | [**Covariant Perturbation Theory (IV). Third Order in the Curvature** — A. O. Barvinsky, Yu. V. Gusev, G. A. Vilkovisky, V. V. Zhytnikov (2009); arXiv:0911.1168](https://arxiv.org/abs/0911.1168) | Important nonlocal/covariant effective-action machinery beyond local heat-kernel expansions. | `download_arxiv` |
| T1 | [**One-loop divergencies in the theory of gravitation** — G. 't Hooft, M. Veltman (1974); DOI:10.1007/BF01646064](https://doi.org/10.1007/BF01646064) | Classic one-loop divergence result for gravity coupled to matter. | `metadata_and_abstract_unless_licensed` |
| T1 | [**Quantum gravity at two loops** — Marc H. Goroff, Augusto Sagnotti (1985); DOI:10.1016/0370-2693(85)91470-4](https://doi.org/10.1016/0370-2693(85)91470-4) | Canonical explicit demonstration of perturbative nonrenormalizability at two loops. | `metadata_and_abstract_unless_licensed` |
| T1 | [**Renormalization of Higher-Derivative Quantum Gravity** — K. S. Stelle (1977); DOI:10.1103/PhysRevD.16.953](https://doi.org/10.1103/PhysRevD.16.953) | Foundational higher-derivative gravity and renormalizability reference. | `metadata_and_abstract_unless_licensed` |
| T0 | [**Quantum Fields in Curved Space** — N. D. Birrell, P. C. W. Davies (1982); DOI:10.1017/CBO9780511622632](https://www.cambridge.org/core/books/quantum-fields-in-curved-space/95376B0CAD78EE767FCD6205F8327F4C) | Canonical curved-spacetime QFT book. | `metadata_only_until_licensed_copy` |
| T0 | [**Quantum Field Theory in Curved Spacetime: Quantized Fields and Gravity** — Leonard Parker, David Toms (2009); DOI:10.1017/CBO9780511813924](https://www.cambridge.org/core/books/quantum-field-theory-in-curved-spacetime/DDFF5C8EAF145364DAC04BDA0B79C624) | Modern detailed curved-QFT treatment, including one-loop effective actions. | `metadata_only_until_licensed_copy` |
| T0 | [**Heat Kernel and Quantum Gravity** — Ivan G. Avramidi (2000); DOI:10.1007/3-540-46523-5](https://doi.org/10.1007/3-540-46523-5) | Advanced systematic heat-kernel reference highly relevant to symbolic curved-space calculations. | `metadata_only_until_licensed_copy` |
| T1 | [**Introduction to Quantum Field Theory with Applications to Quantum Gravity** — I. L. Buchbinder, I. L. Shapiro (2021); DOI:10.1093/oso/9780198838319.001.0001](https://doi.org/10.1093/oso/9780198838319.001.0001) | Modern bridge between QFT techniques and perturbative quantum gravity. | `metadata_only_until_licensed_copy` |

## Spin-2 consistency, emergent gravity and preferred structures

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T0 | [**Self-Interaction and Gauge Invariance** — Stanley Deser (1970); arXiv:gr-qc/0411023; DOI:10.1007/BF00759198](https://arxiv.org/abs/gr-qc/0411023) | Canonical derivation of nonlinear gravity from consistent self-coupling of a massless spin-2 field. | `download_arxiv` |
| T0 | [**Limits on Massless Particles** — Steven Weinberg, Edward Witten (1980); DOI:10.1016/0370-2693(80)90212-9](https://doi.org/10.1016/0370-2693(80)90212-9) | Essential no-go constraint on composite/emergent massless spin-2 scenarios. | `metadata_and_abstract_unless_licensed` |
| T1 | [**Resummation of Massive Gravity** — Claudia de Rham, Gregory Gabadadze, Andrew J. Tolley (2010); arXiv:1011.1232](https://arxiv.org/abs/1011.1232) | Foundational ghost-free nonlinear massive gravity. | `download_arxiv` |
| T0 | [**Massive Gravity** — Claudia de Rham (2014); arXiv:1401.4173](https://arxiv.org/abs/1401.4173) | Comprehensive spin-2/massive-gravity reference for consistency constraints. | `download_arxiv` |
| T1 | [**Einstein-Aether Theory** — Christopher Eling, Ted Jacobson, David Mattingly (2004); arXiv:gr-qc/0410001](https://arxiv.org/abs/gr-qc/0410001) | Key reference for gravitational theories with a preferred timelike structure. | `download_arxiv` |
| T1 | [**Horava-Lifshitz Cosmology: A Review** — Shinji Mukohyama (2010); arXiv:1007.5199](https://arxiv.org/abs/1007.5199) | Representative preferred-foliation UV modification of gravity. | `download_arxiv` |
| T1 | [**Sakharov's induced gravity: a modern perspective** — Matt Visser (2002); arXiv:gr-qc/0204062](https://arxiv.org/abs/gr-qc/0204062) | Useful precedent for gravity emerging as an induced low-energy effect. | `download_arxiv` |
| T1 | [**Composite graviton self-interactions in a model of emergent gravity** — Christopher D. Carone, Joshua Erlich, Marc Sher (2017); arXiv:1710.09367](https://arxiv.org/abs/1710.09367) | Concrete composite-graviton model relevant to emergent-spin-2 directions. | `download_arxiv` |

## Classical gravity, amplitudes and observables

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T0 | [**An Effective Field Theory of Gravity for Extended Objects** — Walter D. Goldberger, Ira Z. Rothstein (2004); arXiv:hep-th/0409156](https://arxiv.org/abs/hep-th/0409156) | Foundational worldline EFT for compact-object dynamics. | `download_arxiv` |
| T0 | [**The effective field theorist's approach to gravitational dynamics** — Rafael A. Porto (2016); arXiv:1601.04914](https://arxiv.org/abs/1601.04914) | Broad EFT treatment of gravitational dynamics and observables. | `download_arxiv` |
| T1 | [**Effective Field Theories of Post-Newtonian Gravity: A comprehensive review** — Michele Levi (2018); arXiv:1807.01699](https://arxiv.org/abs/1807.01699) | Detailed PN EFT reference complementary to amplitude/PM methods. | `download_arxiv` |
| T0 | [**SAGEX Review on Scattering Amplitudes, Chapter 13: Post-Minkowskian expansion from Scattering Amplitudes** — N. E. J. Bjerrum-Bohr, Poul H. Damgaard, Ludovic Planté, Pierre Vanhove (2022); arXiv:2203.13024](https://arxiv.org/abs/2203.13024) | Direct bridge from amplitudes to PM conservative observables. | `download_arxiv` |
| T0 | [**SAGEX Review on Scattering Amplitudes, Chapter 14: Classical Gravity from Scattering Amplitudes** — David A. Kosower, Ricardo Monteiro, Donal O'Connell (2022); arXiv:2203.13025](https://arxiv.org/abs/2203.13025) | Core amplitude-based classical-gravity review. | `download_arxiv` |
| T1 | [**Classical Gravity from Loop Amplitudes** — N. E. J. Bjerrum-Bohr, Poul H. Damgaard, Ludovic Planté, Pierre Vanhove (2021); arXiv:2104.04510](https://arxiv.org/abs/2104.04510) | Concrete loop-amplitude route to classical gravitational dynamics. | `download_arxiv` |
| T1 | [**Post-Minkowskian Effective Field Theory for Conservative Binary Dynamics** — Gregor Kälin, Rafael A. Porto (2020); arXiv:2006.01184](https://arxiv.org/abs/2006.01184) | Useful EFT formalism for mapping gravitational interactions to PM dynamics. | `download_arxiv` |
| T1 | [**Scattering Amplitudes and the Conservative Hamiltonian for Binary Systems at Third Post-Minkowskian Order** — Zvi Bern, Clifford Cheung, Radu Roiban, Chia-Hsien Shen, Mikhail P. Solon, Mao Zeng (2019); arXiv:1901.04424](https://arxiv.org/abs/1901.04424) | Landmark demonstration of amplitude methods producing high-order classical binary dynamics. | `download_arxiv` |
| T1 | [**Snowmass White Paper: Gravitational Waves and Scattering Amplitudes** — Alessandra Buonanno, Mohammed Khalil, Donal O'Connell, Radu Roiban, Mikhail P. Solon, Mao Zeng (2022); arXiv:2204.05194](https://arxiv.org/abs/2204.05194) | Relevant bridge between amplitude methods and radiative observables. | `download_arxiv` |
| T1 | [**Revisiting the matching of black hole tidal responses: a systematic study of relativistic and logarithmic corrections** — Mikhail M. Ivanov, Zihan Zhou (2022); arXiv:2208.08459](https://arxiv.org/abs/2208.08459) | Example of matching EFT coefficients to physical compact-object response. | `download_arxiv` |

## Quantum-gravity / FRG landscape

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T0 | [**The Functional Renormalization Group in Quantum Gravity** — Frank Saueressig (2023); arXiv:2302.14152](https://arxiv.org/abs/2302.14152) | Primary modern background for a symbolic FRG/asymptotic-safety direction. | `download_arxiv` |
| T2 | [**Perturbative Asymptotic Safety and Its Phenomenological Applications** — Alexander Bednyakov, Alena Mukhaeva (2023); arXiv:2309.08258](https://arxiv.org/abs/2309.08258) | Useful complementary view of perturbative asymptotic safety. | `download_arxiv` |
| T2 | [**Critical reflections on asymptotically safe gravity** — Alfio Bonanno et al. (2020); arXiv:2004.06810](https://arxiv.org/abs/2004.06810) | Important critical counterweight to pro-asymptotic-safety literature. | `download_arxiv` |
| T2 | [**Quantum Gravity from Causal Dynamical Triangulations: A Review** — Renate Loll (2019); arXiv:1905.08669](https://arxiv.org/abs/1905.08669) | Representative review of a major nonperturbative quantum-gravity program. | `download_arxiv` |
| T2 | [**Loop Quantum Gravity and Quantum Information** — Eugenio Bianchi, Etera R. Livine (2023); arXiv:2302.05922](https://arxiv.org/abs/2302.05922) | Modern LQG overview useful for broad quantum-gravity comparison questions. | `download_arxiv` |
| T1 | [**Quantum Gravity, Third Edition** — Claus Kiefer (2012); DOI:10.1093/acprof:oso/9780199585205.001.0001](https://doi.org/10.1093/acprof:oso/9780199585205.001.0001) | Broad graduate-level quantum-gravity reference. | `metadata_only_until_licensed_copy` |
| T1 | [**An Introduction to Covariant Quantum Gravity and Asymptotic Safety** — Roberto Percacci (2017); DOI:10.1142/10369](https://doi.org/10.1142/10369) | Technical asymptotic-safety and covariant quantum-gravity reference. | `metadata_only_until_licensed_copy` |

## Computational tools worth indexing

| Tier | Reference | Why it belongs | Ingestion |
|---|---|---|---|
| T2 | [**FeynCalc 10: Do multiloop integrals dream of computer codes?** — Vladyslav Shtabovenko, Rolf Mertig, Frederik Orellana (2023); arXiv:2312.14089](https://arxiv.org/abs/2312.14089) | Major symbolic QFT package relevant for automated calculations and validation. | `download_arxiv` |
| T2 | [**Package-X: A Mathematica package for the analytic calculation of one-loop integrals** — Hiren H. Patel (2015); arXiv:1503.01469](https://arxiv.org/abs/1503.01469) | Useful one-loop analytic integration tool and comparison point for Mathematica workflows. | `download_arxiv` |
| T2 | [**xTras: A field-theory inspired xAct package for Mathematica** — Thomas Nutma (2013); arXiv:1308.3493](https://arxiv.org/abs/1308.3493) | Relevant symbolic tensor/gravity tooling in Mathematica. | `download_arxiv` |
| T2 | [**FIRE6: Feynman Integral REduction with Modular Arithmetic** — A. V. Smirnov, F. S. Chuharev (2019); arXiv:1901.07808](https://arxiv.org/abs/1901.07808) | Representative high-performance IBP reduction tool for future multiloop extensions. | `download_arxiv` |
| T2 | [**Kira 2.0: A novel framework for Feynman integral reduction** — J. Klappert, F. Lange, P. Maierhöfer, J. Usovitsch (2020); arXiv:2008.06494](https://arxiv.org/abs/2008.06494) | Alternative modern IBP reduction infrastructure for multiloop workflows. | `download_arxiv` |

## Highest-priority prior-art cluster for inverse EFT → UV reconstruction

- **Effective description of general extensions of the Standard Model: the complete tree-level dictionary** (2017): Direct precedent for systematic mapping from low-energy EFT operators to broad classes of UV completions.
- **Towards the one loop IR/UV dictionary in the SMEFT: one loop generated operators from new scalars and fermions** (2023): Introduces SOLD and explicitly targets one-loop IR/UV dictionaries.
- **From the EFT to the UV: the complete SMEFT one-loop dictionary** (2024): Closest current precedent to automated inverse UV reconstruction; published in SciPost Physics in 2026.
- **Field redefinitions in effective theories at higher orders** (2018): Essential for inverse matching that must quotient physically redundant descriptions.
- **A Proof of Concept for Matchete: An Automated Tool for Matching Effective Theories** (2022): Central automated functional matching tool and key infrastructure for the planned gravity work.
- **Matchmakereft: automated tree-level and one-loop matching** (2021): Major general automated matching system; essential comparison point.
- **An Efficient On-shell Framework for EFT Matching** (2025): Current on-shell alternative to functional/diagrammatic matching, designed with automation in mind.

## Highest-priority cluster for automated matching with gravity

- **The Universal One-Loop Effective Action with Gravity** (2023): One of the most directly relevant papers for automated one-loop matching with gravity.
- **Covariant derivative expansion for the renormalization of gravity** (2019): Direct bridge between CDE methods and gravitational renormalization.
- **Heat kernel expansion: user's manual** (2003): Canonical practical reference for heat-kernel coefficients and one-loop effective actions.
- **Gravity-Matter Feynman Rules for any Valence** (2020): Directly useful for higher graviton–matter vertices and automated gravity matching.
- **The Fermionic Universal One-Loop Effective Action** (2020): Universal one-loop structures involving heavy fermions; directly useful for heavy-fermion gravity matching.
- **Effective Field Theory of Gravity to All Orders** (2019): Systematic gravitational EFT operator classification; important for arbitrary-order gravity EFT targets.
- **A Proof of Concept for Matchete: An Automated Tool for Matching Effective Theories** (2022): Central automated functional matching tool and key infrastructure for the planned gravity work.

## Bundle contents

- `../../knowledge/references.yaml` — canonical machine-readable Jarvis manifest.
- `seed_corpus.json` — equivalent JSON export.
- `../searches.yaml` — proposed continuous search/watch queries.
- `../../scripts/download_open_arxiv.py` — downloader for official arXiv PDFs only.
