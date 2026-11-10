import posts from '../../../public/data/social_posts.json'
export default defineEventHandler(event => {
  const q = getQuery(event)
  const page = Math.max(1, Math.floor(Number(q.page) || 1))
  const limit = Math.min(10, Math.max(1, Math.floor(Number(q.limit) || 5)))
  const start = (page - 1) * limit
  return {data: posts.slice(start,start+limit),
    paging: {page, limit, next: start+limit < posts.length ? `/api/graph/posts?page=${page+1}&limit=${limit}` : null}}
})
