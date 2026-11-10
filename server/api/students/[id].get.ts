import { studentStore } from '../../utils/store'
export default defineEventHandler(event => {
  const id = Number(getRouterParam(event,'id'))
  const student = studentStore.get(id)
  if (!student) throw createError({statusCode:404,statusMessage:'Student not found'})
  return student
})
