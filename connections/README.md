# Question 5 Six Degrees of Seperation

### Endpoint spec and recommendation.
The endpoint would look like `connections/seperation/<person_id>?degrees=amount`
 * `person_id` The id of the valid person to look up on
 * `degrees` The amount we want to look within to provide the amount of degrees of seperation

 The endpoint would need to make sure it's a valid person id then once that is constructed it should then ensure that the user has the required amount of connections. It would be recommended that first we establish a mutual connections table or something similar that would generate a list containing all the mutual connections between the two connections.
 Example:
  * Tom is connecto to Roy their connection type is a parent, we then search each of their connections to see if Tom has   any connections that also have Roy in any of their connections and store that data for a faster retrieval.
 Once that is created we can then return the list of connections containing the amount requested.

### Technical Challenges.
 * Potentionally highly resource expensive and also long processing time if their already isn't any look up table to draw from.
 * Their might not be any results depending on the contents of the database i.e the amount of people we have in the database. The more people the likier the results.

### Questions for Product Owner
 * How would the data be used? This can impact the structure of the return type that could prevent any more lookups.
 * What should happen if the person does not have the degrees requested?
 * What if the person has more than the required amount? Should their be a priority in which the amount of people returned be ordered?