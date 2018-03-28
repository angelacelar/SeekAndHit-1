if redis.call("EXISTS", "free_parking") == 1 then
  redis.call("DEL", "free_parking");
end

if redis.call("EXISTS", "plane_hash") == 1 then
  redis.call("DEL", "plane_hash");
end

for i=1,99 do
  redis.call("SADD", "free_parking", i)
end
