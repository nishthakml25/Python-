class MemoryBlock:
    def __init__(self, start, size, process=None):
        self.start = start
        self.size = size
        self.process = process
        self.next = None


class MemoryAllocationSimulator:
    def __init__(self, total_memory):
        self.head = MemoryBlock(0, total_memory)

    def display(self):
        current = self.head
        print("\n--- Memory Status ---")

        while current:
            status = "Free" if current.process is None else current.process
            print(
                f"Start: {current.start} KB | "
                f"Size: {current.size} KB | "
                f"Status: {status}"
            )
            current = current.next

    def allocate(self, process, size, method="first"):
        blocks = []
        current = self.head

        while current:
            if current.process is None and current.size >= size:
                blocks.append(current)
            current = current.next

        if not blocks:
            print(f"❌ Not enough memory for {process}")
            return

        if method == "first":
            block = blocks[0]

        elif method == "best":
            block = min(blocks, key=lambda x: x.size)

        elif method == "worst":
            block = max(blocks, key=lambda x: x.size)

        else:
            print("Invalid allocation method!")
            return

        if block.size == size:
            block.process = process

        else:
            new_block = MemoryBlock(
                block.start + size,
                block.size - size
            )

            new_block.next = block.next
            block.next = new_block

            block.size = size
            block.process = process

        print(f"✅ {process} allocated {size} KB using {method.title()} Fit.")

    def deallocate(self, process):
        current = self.head
        found = False

        while current:
            if current.process == process:
                current.process = None
                found = True
                print(f"✅ {process} deallocated successfully.")
                break
            current = current.next

        if not found:
            print(f"❌ Process {process} not found.")

        self.merge_free_blocks()

    def merge_free_blocks(self):
        current = self.head

        while current and current.next:
            if current.process is None and current.next.process is None:
                current.size += current.next.size
                current.next = current.next.next
            else:
                current = current.next


# ---------------- MAIN PROGRAM ----------------

memory = MemoryAllocationSimulator(1024)

while True:
    print("\n===== MEMORY ALLOCATION SIMULATOR =====")
    print("1. Allocate Memory")
    print("2. Deallocate Memory")
    print("3. Display Memory")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        process = input("Enter process name: ")
        size = int(input("Enter memory size (KB): "))

        print("\nAllocation Methods:")
        print("1. First Fit")
        print("2. Best Fit")
        print("3. Worst Fit")

        method_choice = input("Choose method: ")

        methods = {
            "1": "first",
            "2": "best",
            "3": "worst"
        }

        method = methods.get(method_choice)

        if method:
            memory.allocate(process, size, method)
        else:
            print("❌ Invalid method.")

    elif choice == "2":
        process = input("Enter process name to deallocate: ")
        memory.deallocate(process)

    elif choice == "3":
        memory.display()

    elif choice == "4":
        print("Thank you for using Memory Allocation Simulator!")
        break

    else:
        print("❌ Invalid choice.")
