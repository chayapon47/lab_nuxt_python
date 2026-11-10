import students from '../../../data/students.json'
export default defineEventHandler(event => {
  const q = getQuery(event)
  const faculty = typeof q.faculty === 'string' ? q.faculty.toLowerCase() : ''
  const result = students.filter(s => !faculty || s.faculty.toLowerCase() === faculty)
  return {source:'json',count:result.length,data:result}
})
