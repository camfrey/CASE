db.listingsAndReviews.aggregate([
  {
    $search: {
      "text": {
        "query": "garden",
        "path": "name"
      }
    }
  },
  {
    $project: {
      name: 1,
      score: { $meta: "searchScore" }
    }
  }
])

db.listingsAndReviews.aggregate([
  {
    $search: {
      index: 'default',
      text: {
        query: 'duplex',
        path: {
          'wildcard': '*'
        }
      }
    }
  }
])

db.listingsAndReviews.aggregate([
    {$limit: 5}
])

db.customers.aggregate([
  {$limit: 5}
])

db.customers.aggregate([
  {
    $search: {
      index: 'defaulta',
      text: {
        query: 'dana',
        path: {
          'wildcard': '*'
        }
      }
    }
  }
])