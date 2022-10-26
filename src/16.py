
import math

class Transmission():
    def __init__(self, transmission) -> None:
        self.root_packet_data = f'{int(transmission, 16):b}'.zfill(len(transmission) * 4)
        self.root_packet = Packet.create_packet(self.root_packet_data)

    def calc_version_sum(self):
        return self.root_packet.calc_version_sum()

    def evaluate(self):
        return self.root_packet.evaluate()


class Packet():
    def __init__(self, packet_data) -> None:
        self.version = int(packet_data[:3], 2)
        self.type_id = int(packet_data[3:6], 2) 
        self.packet = packet_data

    def __len__(self):
        return len(self.packet)

    @staticmethod
    def create_packet(packet_data):
        type_id = int(packet_data[3:6], 2)
        if type_id == 4:
            return LiteralValuePacket(packet_data)
        else:
            return OperatorPacket(packet_data)


class OperatorPacket(Packet):
    def __init__(self, packet_data) -> None:
        super().__init__(packet_data)
        self.length_type_id = packet_data[6]
        self.contained_packets = []
        self.packet = packet_data[:7]

        if self.length_type_id == '0':
            end_meta_loc = 7 + 15
            total_content_length_binary = packet_data[7:end_meta_loc]
            total_content_length = int(total_content_length_binary, 2)
            self.content = packet_data[end_meta_loc:end_meta_loc + total_content_length]
            self.packet += total_content_length_binary + self.content

            bits_parsed = 0
            while bits_parsed < total_content_length:
                remaining_bits = self.content[bits_parsed:]
                new_packet = Packet.create_packet(remaining_bits)
                self.contained_packets.append(new_packet)
                bits_parsed += len(new_packet)
        else:
            end_meta_loc = 7 + 11
            total_contained_packets_binary = packet_data[7:end_meta_loc]
            total_contained_packets = int(total_contained_packets_binary, 2)
            potential_content = packet_data[end_meta_loc:]
            self.content = ''

            bits_parsed = 0
            for _ in range(total_contained_packets):
                remaining_bits = potential_content[bits_parsed:]
                new_packet = Packet.create_packet(remaining_bits)
                self.contained_packets.append(new_packet)
                bits_parsed += len(new_packet)
                self.content += new_packet.packet
            
            self.packet += total_contained_packets_binary + self.content

    def __repr__(self) -> str:
        return f'Op({self.type_id}, {str(self.contained_packets)})'

    def calc_version_sum(self):
        total_version_sum = self.version

        for i in self.contained_packets:
            total_version_sum += i.calc_version_sum()

        return total_version_sum

    def evaluate(self):
        if self.type_id == 0:
            return sum([i.evaluate() for i in self.contained_packets])
        if self.type_id == 1:
            return math.prod([i.evaluate() for i in self.contained_packets])
        if self.type_id == 2:
            return min([i.evaluate() for i in self.contained_packets])
        if self.type_id == 3:
            return max([i.evaluate() for i in self.contained_packets])
        if self.type_id == 5:
            return int(self.contained_packets[0].evaluate() > self.contained_packets[1].evaluate())
        if self.type_id == 6:
            return int(self.contained_packets[0].evaluate() < self.contained_packets[1].evaluate())
        if self.type_id == 7:
            return int(self.contained_packets[0].evaluate() == self.contained_packets[1].evaluate())
            


class LiteralValuePacket(Packet):
    def __init__(self, packet_data) -> None:
        super().__init__(packet_data)

        self.packet = packet_data[:6]
        possible_contents = packet_data[6:]
        binary_literal_value = ''
        bit_group_size = 5
        for i in range(0, len(possible_contents), bit_group_size):
            group = possible_contents[i: i + bit_group_size]
            
            binary_literal_value += group[1:]
            self.packet += group

            if possible_contents[i] == '0':
                break

        self.literal_value = int(binary_literal_value, 2)
        self.content = binary_literal_value

    def __repr__(self) -> str:
        return f'Literal({self.type_id}, {self.literal_value})'

    def calc_version_sum(self):
        return self.version

    def evaluate(self):
        return self.literal_value


if __name__ == "__main__":    
    with open('src/16.txt') as file:
        transmission_str = file.read()

    transmission = Transmission(transmission_str)

    print(transmission.root_packet)

    print(f'part 1 answer is: {transmission.calc_version_sum()}')

    print(f'part 2 answer is: {transmission.evaluate()}')