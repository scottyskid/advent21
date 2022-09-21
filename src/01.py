

def sliding_sum(num_list: list, window_size: int = 3):
    sum_list = []
    for i in range(len(num_list) - window_size + 1):
        sum_list.append(sum(num_list[i: i + window_size]))

    return sum_list


def count_increases(num_list: list):
    increases = 0

    current_depth = num_list[0]
    for num in num_list[1:]:
        
        if int(num) > current_depth:
            increases += 1
        current_depth = int(num)

    return increases



if __name__ == "__main__":
    

    with open('src/01.txt') as file:
        nums = [int(i) for i in file]
    
    increases = count_increases(nums) 
    
    print(f'number of increases part 1: {increases}')

    sliding_sum_result = sliding_sum(nums)
    increases = count_increases(sliding_sum_result)

    print(f'number of increases part 2: {increases}')
