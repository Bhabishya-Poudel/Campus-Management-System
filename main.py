from collections import deque


class service_Request:
    def __init__(self, requestId, requestName, requestCategory, requestDescription, requestPriority, requestStatus):
        self.request_Id = requestId
        self.request_Name = requestName
        self.request_Category = requestCategory
        self.request_Description = requestDescription
        self.request_Priority = requestPriority
        self.request_Status = requestStatus

    def displayRequest(self):
        print("Request ID:", self.request_Id)
        print("Name:", self.request_Name)
        print("Category:", self.request_Category)
        print("Description:", self.request_Description)
        if self.request_Priority is not None:
            print("Priority:", self.request_Priority)
        print("Status:", self.request_Status)


class bstNode:
    def __init__(self, request):
        self.request_Id = request.request_Id
        self.request = request
        self.left = None
        self.right = None


class requestQueue:
    def __init__(self):
        self.requests = deque()
        self.urgent_heap = []
        self.counter = 0
        self.Pending = []
        self.Completed = []
        self.root = None

    def insertUrgent(self, entry):
        self.urgent_heap.append(entry)
        index = len(self.urgent_heap) - 1

        # Sift up: swap with the parent while this entry is smaller.
        while index > 0:
            parent = (index - 1) // 2
            if self.urgent_heap[index] >= self.urgent_heap[parent]:
                break
            self.urgent_heap[index], self.urgent_heap[parent] = self.urgent_heap[parent], self.urgent_heap[index]
            index = parent

    def removeUrgent(self):
        if not self.urgent_heap:
            raise IndexError("Cannot remove from an empty heap")

        first = self.urgent_heap[0]
        last = self.urgent_heap.pop()
        if not self.urgent_heap:
            return first

        self.urgent_heap[0] = last
        index = 0

        # Sift down: swap with the smaller child until correctly placed.
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < len(self.urgent_heap) and self.urgent_heap[left] < self.urgent_heap[smallest]:
                smallest = left
            if right < len(self.urgent_heap) and self.urgent_heap[right] < self.urgent_heap[smallest]:
                smallest = right
            if smallest == index:
                break

            self.urgent_heap[index], self.urgent_heap[smallest] = self.urgent_heap[smallest], self.urgent_heap[index]
            index = smallest

        return first

    def addToBST(self, request):
        if self.root is None:
            self.root = bstNode(request)
            return True

        current = self.root
        while current is not None:
            if request.request_Id == current.request_Id:
                return False
            elif request.request_Id < current.request_Id:
                if current.left is None:
                    current.left = bstNode(request)
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = bstNode(request)
                    return True
                current = current.right

    def searchRequest(self, requestId):
        current = self.root
        while current is not None:
            if requestId == current.request_Id:
                print("Request found!")
                return current.request
            elif requestId < current.request_Id:
                current = current.left
            else:
                current = current.right
        print("Request not found!")
        return None

    def getPending(self):
        return self.Pending

    def displayNormalRequests(self):
        if self.requests:
            for request in self.requests:
                request.displayRequest()
        else:
            print("There are no pending normal requests!")

    def displayUrgentRequests(self):
        if self.urgent_heap:
            for entry in sorted(self.urgent_heap):
                entry[2].displayRequest()
        else:
            print("There are no pending urgent requests!")

    def displayCompletedRequests(self):
        if self.Completed:
            for entry in self.Completed:
                if entry[0] == "normal":
                    entry[1].displayRequest()
                else:
                    entry[1][2].displayRequest()
        else:
            print("There are no completed requests yet!")

    def displayStatistics(self):
        print("Total requests:", len(self.Pending) + len(self.Completed))
        print("Pending requests:", len(self.Pending))
        print("Completed requests:", len(self.Completed))
        print("Pending normal requests:", len(self.requests))
        print("Pending urgent requests:", len(self.urgent_heap))

    def viewCompleted(self):
        if self.Completed:
            entry = self.Completed[-1]
            if entry[0] == "normal":
                return entry[-1]
            else:
                return entry[-1][2]
        else:
            print("There are no completed requests yet!")

    def undoCompleted(self):
        if self.Completed:
            flag, data = self.Completed.pop()
            if flag == "urgent":
                data[2].request_Status = "Pending"
                self.insertUrgent(data)
                self.Pending.append(data[2])

    def addNormalRequest(self, srClass): #srClass data type is a class of Service_request
        if self.addToBST(srClass) == False:
            return False
        srClass.request_Status = "Pending"
        srClass.request_Priority = None
        self.requests.append(srClass)
        self.Pending.append(srClass)
        return True

    def addUrgentRequest(self, priority, request): #request data type is a class of Service_request
        if self.addToBST(request) == False:
            return False
        self.counter += 1
        request.request_Status = "Pending"
        self.insertUrgent((priority, self.counter, request))
        self.Pending.append(request)
        return True

    def ProcessRequest(self):
        if self.urgent_heap:
            urgentRequest = self.removeUrgent()
            urgentRequest[2].request_Status = "Completed"
            self.Completed.append(("urgent", urgentRequest)) #urgentRequest is the full (priority, counter, request) tuple
            self.Pending.remove(urgentRequest[2])
        elif self.requests:
            normalRequest = self.requests.popleft()
            normalRequest.request_Status = "Completed"
            self.Completed.append(("normal", normalRequest)) #store entire class, not just request
            self.Pending.remove(normalRequest)
        else:
            print("There are no pending requests to process!")
 

def getNumber(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number > 0:
                return number
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Please enter a whole number.")


q = requestQueue()

while True:
    print("\nCampus Service Management System")
    print("1. Add Normal Request")
    print("2. Add Urgent Request")
    print("3. Process Next Request")
    print("4. Search for Request")
    print("5. View Pending Requests")
    print("6. View Completed Requests")
    print("7. View Statistics")
    print("8. Exit")

    choice = input("Enter your choice (1-8): ").strip()

    if choice == "1" or choice == "2":
        requestId = getNumber("Request ID: ")
        requestName = input("Name: ").strip()
        requestCategory = input("Category: ").strip()
        requestDescription = input("Description: ").strip()
        priority = None # Normal requests use arrival order.

        if choice == "2":
            while True:
                priority = getNumber("Priority (1-5, 1 is most urgent): ")
                if priority >= 1 and priority <= 5:
                    break
                print("Please enter a priority between 1 and 5.")

        request = service_Request(requestId, requestName, requestCategory, requestDescription, priority, "Pending")

        if choice == "1":
            added = q.addNormalRequest(request)
        else:
            added = q.addUrgentRequest(priority, request)

        if added:
            print("Request added successfully!")
        else:
            print("A request with this ID already exists!")

    elif choice == "3":
        if q.Pending:
            q.ProcessRequest()
            print("Request completed:")
            q.viewCompleted().displayRequest()
        else:
            q.ProcessRequest()

    elif choice == "4":
        requestId = getNumber("Enter the Request ID to search: ")
        request = q.searchRequest(requestId)
        if request is not None:
            request.displayRequest()

    elif choice == "5":
        print("\nPending Normal Requests")
        q.displayNormalRequests()
        print("\nPending Urgent Requests")
        q.displayUrgentRequests()

    elif choice == "6":
        print("\nCompleted Requests")
        q.displayCompletedRequests()

    elif choice == "7":
        print("\nSystem Statistics")
        q.displayStatistics()

    elif choice == "8":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please choose a number from 1 to 8.")

    input("\nPress Enter to return to the menu...")
