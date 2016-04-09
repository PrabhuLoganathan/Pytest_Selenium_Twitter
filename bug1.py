# def test_make_error(auth1,auth2,user_info,create_friend,destroy_friend):
# 	user2 = UserKeys().user2() # get user 2's info from hidden class
# 	follow_data1 = create_friend(auth1,screen_name=user2["screen_name"])# user1 follows user2
# 	unfollow_data1 = destroy_friend(auth1, screen_name=user2["screen_name"]) # user1 unfollows user2

# 	follow_data2 = create_friend(auth1,user_id=user2["user_id"])# user1 follows user2
# 	unfollow_data2 = destroy_friend(auth1, user_id=user2["user_id"]) # user1 unfollows user2
# 	print '***************************************************************************'
# 	print "Create with screen_name: "
# 	print "Follow data: "
# 	print follow_data1
# 	print
# 	print "Unfollow Data: "
# 	print unfollow_data1
# 	print
# 	print '***************************************************************************'
# 	print "Create with user_id: "
# 	print "Follow data: "
# 	print follow_data2
# 	print
# 	print "Unfollow Data: "
# 	print unfollow_data2
# 	print