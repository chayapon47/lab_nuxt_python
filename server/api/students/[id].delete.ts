import { studentStore } from '../../utils/store'
export default defineEventHandler(event => {
  const id = Number(getRouterParam(event,'id'))
  if (!studentStore.delete(id)) throw createError({statusCode:404,statusMessage:'Student not found'})
  setResponseStatus(event,204)
  return null
})
