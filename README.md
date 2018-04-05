# Relational Functional Gradient Boosting (RFGB)

[![][license img]][license] [![][release img]][release] [![][build img]][build link] [![][codecov img]][codecov link]

RFGB in Python. Inspired by [BoostSRL](https://github.com/boost-starai/BoostSRL).

## Getting Started

**Prerequisites**

* Python (2.7, 3.3, 3.4, 3.5, 3.6)

**Installation**

None currently. Clone the repository with git or download a zip archive, then run the scripts from the command line.

## Sample Usage

1. Logistics

        python src/main.py -target unload -train testDomains/Logistics/train/ -test testDomains/Logistics/test/ -trees 10

**Classification with Expert Advice (-expAdvice)**

Preferred and non-preferred labels may be provided as advice during classification via logical rules. This advice may be specified in a file named `advice.txt` in the train directory for a dataset.

Four datasets (BlocksWorld, HeartAttack, Logistics, and MoodDisorder) have an advice file included.

1. Logistics

        python src/main.py -expAdvice -target unload -train testDomains/Logistics/train/ -test testDomains/Logistics/test/ -trees 10

2. HeartAttack

        python src/main.py -expAdvice -target ha -train testDomains/HeartAttack/train/ -test testDomains/HeartAttack/test/ -trees 10

## Targets

"Targets" specify what is learned, examples of the target are provided in `pos.txt`, `neg.txt`, or `examples.txt` (for regression). These are specified here for convenience.

| **Dataset** | **Target** |
| :---------: | :--------: |
| BlocksWorld | `putdown` |
| BostonHousing | `medv` |
| HeartAttack | `ha` |
| Insurance | `value` |
| Logistics | `unload` |
| MoodDisorder | `bipolar` |
| TicTacToe | `put` or `dontput` |
| ToyCancer | `cancer` |
| XOR | `xor` |

## In Development

* [ ] Test cases (codecov >90%)
* [ ] Learning Markov Logic Networks
* [ ] Learning with Soft-Margin

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

A full [copy of the license](https://github.com/batflyer/RFGB/blob/master/LICENSE) is available in the base of this repository. For more information, see https://www.gnu.org/licenses/

## Acknowledgements

The authors would like to thank Professor Sriraam Natarajan, Professor Gautam Kunapuli, and fellow members of the [StARLinG Lab](https://starling.utdallas.edu) at the University of Texas at Dallas.

[license]:LICENSE
[license img]:https://img.shields.io/github/license/batflyer/RFGB.svg?style=flat-square

[release]: https://github.com/batflyer/RFGB/releases
[release img]:https://img.shields.io/github/tag/batflyer/RFGB.svg?style=flat-square

[build link]:https://travis-ci.org/batflyer/RFGB.svg?branch=master
[build img]:https://img.shields.io/travis/batflyer/RFGB.svg?style=flat-square

[codecov link]:https://codecov.io/gh/batflyer/RFGB?branch=master
[codecov img]:https://img.shields.io/codecov/c/github/batflyer/RFGB/master.svg?style=flat-square
