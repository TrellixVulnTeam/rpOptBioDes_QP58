# rpOptBioDes

Docker implementation of the OptBioDes tool by Pablo Carbonell

## Getting Started

This is a docker galaxy tools, and thus, the docker needs to be built locally where Galaxy is installed. 

## Input

Required information:
* **-input**: (string) Path to either tar.xz input collection of rpSBML files or a single rpSBML file.
* **-input_format**: (string) Format of the input
* **-input_sbol**: (string) Path to the SBOL input file

Advanced options:
* **-pathway_id**: (string, default: rp_pathway) The SBML groups ID (defined in rpReader) that points to the heterologous reactions and chemical species.
* **-max_variants**: (integer, default: 5) Maximal variants for each part 
* **-lib_size**: (integer, default: 102) Maximal library size 
* **-input_parts**: (boolean, default: True) Number of enzymes for each coding sequence

## Output

* **output**: (string) Path to the output SBOL file

## Dependencies

* Base Docker Image: [python:3.6](https://hub.docker.com/_/python)

## Installing

To build the image using the Dockerfile, use the following command:

```
docker build -t brsynth/rpoptbiodes-standalone .
```

### Running the tests

To run the test, untar the test.tar.xz file and run the following command:

```
python run,py -input test/test_rpGlobalScore.tar -input_format tar -input_sbol test/test.sbol -output test/test_output.tar
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

v0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson

### How to cite rpOptBioDes?
