module.exports.add = async ({ x, y }) => {
  return x + y
}

module.exports.double = async ( n ) => {
  return  n * 2
}

module.exports.sample = async function(event, context) {
  console.log('Remaining time: ', context.getRemainingTimeInMillis())
  console.log('Function name: ', context.functionName)
  console.log("EVENT: \n" + JSON.stringify(event, null, 2))
  return context.logStreamName
}

