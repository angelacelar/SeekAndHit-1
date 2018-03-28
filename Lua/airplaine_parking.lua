redis.replicate_commands()

local plane_id = ARGV[1]

if tonumber(plane_id) == nil then
  return 'Plane id is not a number.'
end

if tonumber(plane_id) < 1 or tonumber(plane_id) > 81 then
  return 'Plane id is not in between values of 1 and 80'
end

local items = redis.call('lrange', 'parked_planes', 0, -1)

if redis.call('hget', 'plane_hash', plane_id) then return tonumber(redis.call('hget', 'plane_hash', plane_id)) end

local free = redis.call('srandmember', 'free_parking')
if tonumber(free) == nil then
  return 'No parking spots left'
end

redis.call('hset', 'plane_hash', plane_id, free)
redis.call('srem', 'free_parking', free)

return tonumber(free)
