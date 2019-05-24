import os
import tempfile
import clyngor


root = __file__.rsplit('/', 1)[0]

scope_prg = root + '/encodings/get_scope.lp'
unproducible_prg = root + '/encodings/get_unproducible_targets.lp'
path_prg = root + '/encodings/get_paths.lp'
min_path_prg = root + '/encodings/get_min_paths.lp'
cof_prg =       root + '/encodings/get_cofs.lp'
cof_w_prg =       root + '/encodings/get_cofs_weighted.lp'

def get_scope(draft, seeds):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    prg = [scope_prg, draft_f, seed_f]
    options = ''
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    return best_model


def get_unproducible(draft, seeds, targets):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    target_f = targets.to_file()
    prg = [unproducible_prg, draft_f, seed_f, target_f ]
    options = ''
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(target_f)
    return best_model

def get_paths(instance, min_bool):
    instance_f = instance.to_file()
    if min_bool:
        prg = [min_path_prg, instance_f]
    else:
        prg = [path_prg, instance_f]
    options ='--configuration jumpy --opt-strategy=usc,oll'
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model

    return best_model #models[0]

def get_union_of_paths(instance, optimum, min_bool):
    instance_f = instance.to_file()
    if min_bool:
        prg = [min_path_prg, instance_f]
        options ='--configuration jumpy --opt-strategy=usc,oll --enum-mode=brave --opt-mode=optN,'+str(optimum)
    else:
        prg = [path_prg, instance_f]
        options = '--configuration jumpy --opt-strategy=usc,oll --enum-mode=brave --opt-mode=ignore '
    # solver = Gringo4Clasp(clasp_options=options)
    # union = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model

    os.unlink(instance_f)
    return best_model #union[0]

def get_intersection_of_paths(instance, optimum, min_bool):
    instance_f = instance.to_file()
    if min_bool:
        prg = [min_path_prg, instance_f]
        options = '--configuration jumpy --opt-strategy=usc,oll --enum-mode cautious --opt-mode=optN,' +str(optimum)
    else:
        prg = [path_prg, instance_f]
        options = '--configuration jumpy --opt-strategy=usc,oll --enum-mode cautious --opt-mode=ignore'
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    # solver = Gringo4Clasp(clasp_options=options)
    # intersec = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    #print(os.path.abspath(instance_f))
    os.unlink(instance_f)
    return best_model #intersec[0]

def get_all_paths(instance, optimum, min_bool, nmodels=0):
    instance_f = instance.to_file()
    if min_bool:
        prg = [min_path_prg, instance_f]
        options = '--configuration handy --opt-strategy=usc,oll --opt-mode=optN,' +str(optimum)
    else:
        prg = [path_prg, instance_f]
        options = '--configuration handy --opt-strategy=usc,oll --opt-mode=enum'
    # solver = Gringo4Clasp(clasp_options=options)
    # models = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    models = clyngor.solve(prg, options=options, nb_model=nmodels)
    allmodels = [model for model in models.by_arity.with_optimization]
    os.unlink(instance_f)
    return allmodels

def get_cofs(draft, seeds, targets, cofactors):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    targets_f =  targets.to_file()
    cofactors_f =  cofactors.to_file()
    prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    # solver = Gringo4Clasp()
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    #print(models)
    # print(os.path.abspath(draft_f))
    # print(os.path.abspath(seed_f))
    # print(os.path.abspath(targets_f))
    # print(os.path.abspath(cofactors_f))
    best_model = None
    options = ''
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)

    return best_model #models[0]

def get_cofs_weighted(draft, seeds, targets, cofactors):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    targets_f =  targets.to_file()
    cofactors_f =  cofactors.to_file()
    prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    options ='--configuration jumpy --opt-strategy=usc,oll'
    # solver = Gringo4Clasp(clasp_options='--configuration jumpy --opt-strategy=usc,oll')
    # models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    #print(models)
    # print(os.path.abspath(draft_f))
    # print(os.path.abspath(seed_f))
    # print(os.path.abspath(targets_f))
    # print(os.path.abspath(cofactors_f))
    best_model = None
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return best_model #models[0]

def get_intersection_of_optimal_solutions_cof(draft, seeds, targets, cofactors, optimum, weighted=False):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    targets_f =  targets.to_file()
    cofactors_f =  cofactors.to_file()
    if weighted:
        prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    else:
        prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    options='--configuration jumpy --opt-strategy=usc,oll --enum-mode=cautious --opt-mode=optN,'+str(optimum)
    best_model = None
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    # solver = Gringo4Clasp(clasp_options=options)
    # intersec = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return best_model #models[0]


def get_union_of_optimal_solutions_cof(draft, seeds, targets, cofactors, optimum, weighted=False):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    targets_f =  targets.to_file()
    cofactors_f =  cofactors.to_file()
    if weighted:
        prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    else:
        prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    options='--configuration jumpy --opt-strategy=usc,oll --enum-mode=cautious --opt-mode=optN,'+str(optimum)
    # solver = Gringo4Clasp(clasp_options=options)
    # union = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    best_model = None
    models = clyngor.solve(prg, options=options)
    for model in models.discard_quotes.by_arity.with_optimization:
        best_model = model
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return best_model #models[0]


def get_optimal_solutions_cof(draft, seeds, targets, cofactors, optimum, weighted, nmodels=0):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    targets_f =  targets.to_file()
    cofactors_f =  cofactors.to_file()
    if weighted:
        prg = [cof_w_prg, draft_f, seed_f, targets_f, cofactors_f]
    else:
        prg = [cof_prg, draft_f, seed_f, targets_f, cofactors_f]
    options = '--configuration jumpy --opt-strategy=usc,oll --opt-mode=enum,' +str(optimum)
    # solver = Gringo4Clasp(clasp_options=options)
    # models = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    models = clyngor.solve(prg, options=options)
    # print(os.path.abspath(draft_f), os.path.abspath(seed_f), os.path.abspath(targets_f), os.path.abspath(cofactors_f))
    allmodels = [model for model in models.by_arity.with_optimization]
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(targets_f)
    os.unlink(cofactors_f)
    return allmodels
