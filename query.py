"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise directions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()

# Part 2: Write queries

# Get the brand with the **id** of 8. (use .get() not filter nor filterby)
Brand.query.get(8)

# Get all models with the **name** Corvette and the **brand_name** Chevrolet.
Model.query.filter_by(name='Corvette', brand_name='Chevrolet').all()

# Get all models that are older than 1960.
Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor".
Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands with that were founded in 1903 and that are not yet discontinued.
Brand.query.filter(Brand.founded == 1903, Brand.discontinued.is_(None)).all()

# Get all brands with that are either discontinued or founded before 1950.
Brand.query.filter((Brand.discontinued.isnot(None)) | (Brand.founded < 1950)).all()

# Get any model whose brand_name is not Chevrolet.
Model.query.filter(Model.brand_name != 'Chevrolet').all()

# Fill in the following functions. (See directions for more info.)


def get_model_info(year):
    '''Takes in a year, and prints out each model, brand_name, and brand
    headquarters for that year using only ONE database query.'''

    # I randomly chose 1960 as a test case, which captured the edge case of
    #   model that has a brand_name that isn't in the brands table

    models_from_year = Model.query.filter(Model.year == year)

    for model in models_from_year:
        name = str(model.name)
        brand = str(model.brand_name)
        if model.brand is not None:
            hq = str(model.brand.headquarters)
        else:
            hq = "unknown"
        print "Model: %s, Brand: %s, Brand Headquarters: %s" % (name, brand, hq)


def get_brands_summary():
    '''Prints out each brand name, and each model name for that brand
       using only ONE database query.'''

    brand_grouping = {}
    brand_model_tuples = db.session.query(Model.brand_name, Model.name).all()
    for brand_model in brand_model_tuples:
        brand, model = brand_model
        if brand_grouping.get(brand):
            brand_grouping[brand].append(model)
        else:
            brand_grouping[brand] = [model]
    for grouping in brand_grouping:
        print "\nBrand: %s" % (grouping)
        for model in brand_grouping[grouping]:
            print "model: ", model

# -------------------------------------------------------------------


# Part 2.5: Advanced and Optional
def search_brands_by_name(mystr):
    """Returns a list of Brand objects whose name contains or is the input string"""

    test_string = "%" + mystr + "%"
    Brand.query.filter(Brand.name.like(test_string)).all()


def get_models_between(start_year, end_year):
    """Returns list of Model objects where start_year < model year < end_year"""

    Model.query.filter(Model.year < end_year, Model.year > start_year).all()

# -------------------------------------------------------------------

# Part 3: Discussion Questions (Include your answers as comments.)

# 1. What is the returned value and datatype of ``Brand.query.filter_by(name='Ford')``?
# A query object is returned. Specifically it is of the class BaseQuery in flask_sqlalchemy.
# Its value is the query itself, a question. In order to get the resulting Brand object,
#   the query would need to be evaluated.

# 2. In your own words, what is an association table, and what *type* of relationship
# does an association table manage?
# An association table manages many-to-many relationships, by effectively converting
#   them into a pair of one-to-many relationships. The association table has no
#   real usefulness on its own, i.e., it doesn't store any data associated with
#   the pairing; it just stores the pairings using the primary key of the paired
#   tables as foreign keys in it.
