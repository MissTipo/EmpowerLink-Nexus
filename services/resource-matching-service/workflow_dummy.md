fix(ci): update training step to run train_model and correctly move model artifact

Replaced ai.matching_model with ai.train_model in the train_and_package job.
Moved the generated matching.pkl to ai/artifacts/model.pkl to ensure the
artifact is uploaded correctly for the build_and_deploy job.

fix(ci): update training step to run train_model and correctly move model artifact
fix(ci): correct training step to use ai/build_model.py and generate model artifact


