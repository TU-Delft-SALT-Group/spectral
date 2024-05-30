def pre_mutation(context):
    if context.filename == "response_examples.py":
        context.skip = True

