module.exports.add = async ({ x, y }) => {
  return x + y
}

class NumberTooBig extends Error
{
  constructor(n)
  {
  super(`${n} is too big!`)
  this.name='NumberTooBig'
  Error.captureStackTrace(this, NumberTooBig)
  }
}

module.exports.double = async ( n ) => {
  if(n>50)
  {
    throw new NumberTooBig(n)
  }
  return  n * 2
}

module.exports.doubleBigNumber = async ( n ) => {
   return  n * 2
}



module.exports.sample = async function(event, context) {
  console.log('Remaining time: ', context.getRemainingTimeInMillis())
  console.log('Function name: ', context.functionName)
  console.log("EVENT: \n" + JSON.stringify(event, null, 2))
  return context.logStreamName
}

