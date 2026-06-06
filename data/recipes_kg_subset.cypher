// Module 9 Week B — Stretch Tue — recipes_kg_subset.cypher
//
// Smaller subset (~40 nodes) of the Lab 9B fixture for fast CI on the
// KG critic. Same schema as the lab — every domain node also carries
// :Entity per the Identity Discipline. ids follow '<label-lower>:<slug>'.
//
// Loaded by load_fixture.py, which also asserts the Identity Discipline
// constraint and the expected node/relationship counts.

// --- Constraint -------------------------------------------------------

CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
  FOR (n:Entity) REQUIRE n.id IS UNIQUE;

// --- Cuisines (8) -----------------------------------------------------

MERGE (:Cuisine:Entity {id: 'cuisine:world',     name: 'World'});
MERGE (:Cuisine:Entity {id: 'cuisine:asian',     name: 'Asian'});
MERGE (:Cuisine:Entity {id: 'cuisine:chinese',   name: 'Chinese'});
MERGE (:Cuisine:Entity {id: 'cuisine:sichuan',   name: 'Sichuan'});
MERGE (:Cuisine:Entity {id: 'cuisine:cantonese', name: 'Cantonese'});
MERGE (:Cuisine:Entity {id: 'cuisine:european',  name: 'European'});
MERGE (:Cuisine:Entity {id: 'cuisine:italian',   name: 'Italian'});
MERGE (:Cuisine:Entity {id: 'cuisine:tuscan',    name: 'Tuscan'});

// Cuisine SUBCLASS_OF chains
MATCH (a:Cuisine {id: 'cuisine:sichuan'}),   (b:Cuisine {id: 'cuisine:chinese'})  MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Cuisine {id: 'cuisine:cantonese'}), (b:Cuisine {id: 'cuisine:chinese'})  MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Cuisine {id: 'cuisine:chinese'}),   (b:Cuisine {id: 'cuisine:asian'})    MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Cuisine {id: 'cuisine:asian'}),     (b:Cuisine {id: 'cuisine:world'})    MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Cuisine {id: 'cuisine:tuscan'}),    (b:Cuisine {id: 'cuisine:italian'})  MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Cuisine {id: 'cuisine:italian'}),   (b:Cuisine {id: 'cuisine:european'}) MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Cuisine {id: 'cuisine:european'}),  (b:Cuisine {id: 'cuisine:world'})    MERGE (a)-[:SUBCLASS_OF]->(b);

// --- Ingredients (8) --------------------------------------------------

MERGE (:Ingredient:Entity {id: 'ingredient:spice',              name: 'spice',              category: 'spice'});
MERGE (:Ingredient:Entity {id: 'ingredient:peppercorn',         name: 'peppercorn',         category: 'spice'});
MERGE (:Ingredient:Entity {id: 'ingredient:szechuanpeppercorn', name: 'szechuanPeppercorn', category: 'spice'});
MERGE (:Ingredient:Entity {id: 'ingredient:herb',               name: 'herb',               category: 'herb'});
MERGE (:Ingredient:Entity {id: 'ingredient:basil',              name: 'basil',              category: 'herb'});
MERGE (:Ingredient:Entity {id: 'ingredient:ginger',             name: 'ginger',             category: 'spice'});
MERGE (:Ingredient:Entity {id: 'ingredient:garlic',             name: 'garlic',             category: 'vegetable'});
MERGE (:Ingredient:Entity {id: 'ingredient:tomato',             name: 'tomato',             category: 'vegetable'});

// Ingredient SUBCLASS_OF chains
MATCH (a:Ingredient {id: 'ingredient:szechuanpeppercorn'}), (b:Ingredient {id: 'ingredient:peppercorn'}) MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Ingredient {id: 'ingredient:peppercorn'}),         (b:Ingredient {id: 'ingredient:spice'})      MERGE (a)-[:SUBCLASS_OF]->(b);
MATCH (a:Ingredient {id: 'ingredient:basil'}),              (b:Ingredient {id: 'ingredient:herb'})       MERGE (a)-[:SUBCLASS_OF]->(b);

// --- Authors (4) ------------------------------------------------------

MERGE (:Author:Entity {id: 'author:maria-rossi', name: 'Maria Rossi', country: 'Italy'});
MERGE (:Author:Entity {id: 'author:li-wei',      name: 'Li Wei',      country: 'China'});
MERGE (:Author:Entity {id: 'author:julia-chen',  name: 'Julia Chen',  country: 'USA'});
MERGE (:Author:Entity {id: 'author:antonio-b',   name: 'Antonio B',   country: 'Italy'});

// --- Techniques (3) ---------------------------------------------------

MERGE (:Technique:Entity {id: 'technique:stir-fry', name: 'stir-fry'});
MERGE (:Technique:Entity {id: 'technique:braise',   name: 'braise'});
MERGE (:Technique:Entity {id: 'technique:saute',    name: 'saute'});

// --- Recipes (8) ------------------------------------------------------

MERGE (:Recipe:Entity {id: 'recipe:001', name: 'Mapo Tofu',             description: 'Sichuan classic',         popularityScore: 90, prepMinutes: 30});
MERGE (:Recipe:Entity {id: 'recipe:002', name: 'Dan Dan Noodles',       description: 'Sichuan noodle dish',     popularityScore: 85, prepMinutes: 25});
MERGE (:Recipe:Entity {id: 'recipe:003', name: 'Cantonese Steamed Fish',description: 'Light steamed fish',      popularityScore: 80, prepMinutes: 20});
MERGE (:Recipe:Entity {id: 'recipe:004', name: 'Margherita Pizza',      description: 'Tomato, basil, mozzarella',popularityScore: 95, prepMinutes: 40});
MERGE (:Recipe:Entity {id: 'recipe:005', name: 'Tuscan Ribollita',      description: 'Bread and vegetable soup',popularityScore: 70, prepMinutes: 60});
MERGE (:Recipe:Entity {id: 'recipe:006', name: 'Pasta al Pomodoro',     description: 'Italian tomato pasta',    popularityScore: 88, prepMinutes: 20});
MERGE (:Recipe:Entity {id: 'recipe:007', name: 'Kung Pao Chicken',      description: 'Spicy Sichuan stir-fry',  popularityScore: 92, prepMinutes: 25});
MERGE (:Recipe:Entity {id: 'recipe:008', name: 'Pesto Genovese',        description: 'Basil pesto',             popularityScore: 78, prepMinutes: 15});

// --- Recipe relationships ---------------------------------------------

// OF_CUISINE
MATCH (r:Recipe {id: 'recipe:001'}), (c:Cuisine {id: 'cuisine:sichuan'})   MERGE (r)-[:OF_CUISINE]->(c);
MATCH (r:Recipe {id: 'recipe:002'}), (c:Cuisine {id: 'cuisine:sichuan'})   MERGE (r)-[:OF_CUISINE]->(c);
MATCH (r:Recipe {id: 'recipe:003'}), (c:Cuisine {id: 'cuisine:cantonese'}) MERGE (r)-[:OF_CUISINE]->(c);
MATCH (r:Recipe {id: 'recipe:004'}), (c:Cuisine {id: 'cuisine:italian'})   MERGE (r)-[:OF_CUISINE]->(c);
MATCH (r:Recipe {id: 'recipe:005'}), (c:Cuisine {id: 'cuisine:tuscan'})    MERGE (r)-[:OF_CUISINE]->(c);
MATCH (r:Recipe {id: 'recipe:006'}), (c:Cuisine {id: 'cuisine:italian'})   MERGE (r)-[:OF_CUISINE]->(c);
MATCH (r:Recipe {id: 'recipe:007'}), (c:Cuisine {id: 'cuisine:sichuan'})   MERGE (r)-[:OF_CUISINE]->(c);
MATCH (r:Recipe {id: 'recipe:008'}), (c:Cuisine {id: 'cuisine:italian'})   MERGE (r)-[:OF_CUISINE]->(c);

// USES_INGREDIENT
MATCH (r:Recipe {id: 'recipe:001'}), (i:Ingredient {id: 'ingredient:szechuanpeppercorn'}) MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:001'}), (i:Ingredient {id: 'ingredient:garlic'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:002'}), (i:Ingredient {id: 'ingredient:szechuanpeppercorn'}) MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:002'}), (i:Ingredient {id: 'ingredient:ginger'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:003'}), (i:Ingredient {id: 'ingredient:ginger'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:004'}), (i:Ingredient {id: 'ingredient:tomato'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:004'}), (i:Ingredient {id: 'ingredient:basil'})              MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:005'}), (i:Ingredient {id: 'ingredient:tomato'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:006'}), (i:Ingredient {id: 'ingredient:tomato'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:006'}), (i:Ingredient {id: 'ingredient:garlic'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:007'}), (i:Ingredient {id: 'ingredient:ginger'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:007'}), (i:Ingredient {id: 'ingredient:garlic'})             MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:008'}), (i:Ingredient {id: 'ingredient:basil'})              MERGE (r)-[:USES_INGREDIENT]->(i);
MATCH (r:Recipe {id: 'recipe:008'}), (i:Ingredient {id: 'ingredient:garlic'})             MERGE (r)-[:USES_INGREDIENT]->(i);

// BY_AUTHOR
MATCH (r:Recipe {id: 'recipe:001'}), (a:Author {id: 'author:li-wei'})      MERGE (r)-[:BY_AUTHOR]->(a);
MATCH (r:Recipe {id: 'recipe:002'}), (a:Author {id: 'author:li-wei'})      MERGE (r)-[:BY_AUTHOR]->(a);
MATCH (r:Recipe {id: 'recipe:003'}), (a:Author {id: 'author:li-wei'})      MERGE (r)-[:BY_AUTHOR]->(a);
MATCH (r:Recipe {id: 'recipe:004'}), (a:Author {id: 'author:maria-rossi'}) MERGE (r)-[:BY_AUTHOR]->(a);
MATCH (r:Recipe {id: 'recipe:005'}), (a:Author {id: 'author:antonio-b'})   MERGE (r)-[:BY_AUTHOR]->(a);
MATCH (r:Recipe {id: 'recipe:006'}), (a:Author {id: 'author:maria-rossi'}) MERGE (r)-[:BY_AUTHOR]->(a);
MATCH (r:Recipe {id: 'recipe:007'}), (a:Author {id: 'author:julia-chen'})  MERGE (r)-[:BY_AUTHOR]->(a);
MATCH (r:Recipe {id: 'recipe:008'}), (a:Author {id: 'author:antonio-b'})   MERGE (r)-[:BY_AUTHOR]->(a);

// REQUIRES_TECHNIQUE
MATCH (r:Recipe {id: 'recipe:001'}), (t:Technique {id: 'technique:braise'})   MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
MATCH (r:Recipe {id: 'recipe:002'}), (t:Technique {id: 'technique:stir-fry'}) MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
MATCH (r:Recipe {id: 'recipe:003'}), (t:Technique {id: 'technique:braise'})   MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
MATCH (r:Recipe {id: 'recipe:004'}), (t:Technique {id: 'technique:saute'})    MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
MATCH (r:Recipe {id: 'recipe:005'}), (t:Technique {id: 'technique:braise'})   MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
MATCH (r:Recipe {id: 'recipe:006'}), (t:Technique {id: 'technique:saute'})    MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
MATCH (r:Recipe {id: 'recipe:007'}), (t:Technique {id: 'technique:stir-fry'}) MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
MATCH (r:Recipe {id: 'recipe:008'}), (t:Technique {id: 'technique:saute'})    MERGE (r)-[:REQUIRES_TECHNIQUE]->(t);
