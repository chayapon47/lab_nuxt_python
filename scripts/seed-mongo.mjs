import { MongoClient } from 'mongodb'
import { readFile } from 'node:fs/promises'
const uri=process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017'
const name=process.env.MONGODB_DB || 'nuxt_intern'
const client=new MongoClient(uri,{serverSelectionTimeoutMS:3000})
try {
  await client.connect()
  const db=client.db(name)
  for(const collectionName of ['students','courses','instructors','enrollments','social_pages','social_posts']){
    const data=JSON.parse(await readFile(new URL(`../server/data/${collectionName}.json`,import.meta.url),'utf8'))
    const col=db.collection(collectionName)
    await col.deleteMany({}) // Training seed: resets the local exercise collection.
    if(data.length) await col.insertMany(data)
    const key=collectionName==='students'?'student_id':collectionName==='courses'?'course_id':collectionName==='instructors'?'instructor_id':collectionName==='enrollments'?'enrollment_id':'id'
    await col.createIndex({[key]:1},{unique:true})
    console.log(collectionName,data.length)
  }
} finally {await client.close()}
