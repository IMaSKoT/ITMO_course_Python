def f(nums,target):
    #Проверка на тип nums
    if not isinstance(nums, list):
        return None
    #Проверка, что все элементы в nums типа int
    if not all(isinstance(nums[i], int) for i in range (len(nums))):
        return None
    #Проверка на корректность target
    if not isinstance(target, int):
        return None
    #Основной код
    for i in range (len(nums)):
        for j in range (i+1,len(nums)):
            if nums[i]+nums[j] == target:
                return [i,j]
    return None
