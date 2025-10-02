#Problem: Segment Tree with Lazy Propagation

#Problem Statement:
#You are given an array arr of integers. You need to support two operations efficiently:

#Range Update: Add a value val to all elements in a given range [l, r].

#Range Query: Find the sum of elements in a given range [l, r].

#Example:

#Input: arr = [1, 2, 3, 4, 5]
#Operations:
#update(1, 3, 2) -> arr becomes [1, 4, 5, 6, 5]
#query(0, 2) -> 1 + 4 + 5 = 10
#query(2, 4) -> 5 + 6 + 5 = 16


class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(arr, 0, self.n - 1, 1)
    
    def build(self, arr, start, end, node):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self.build(arr, start, mid, 2 * node)
        self.build(arr, mid + 1, end, 2 * node + 1)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    
    def updateRange(self, l, r, val):
        self._update(0, self.n - 1, l, r, val, 1)
    
    def _update(self, start, end, l, r, val, node):
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2*node] += self.lazy[node]
                self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0
        
        if start > r or end < l:
            return
        
        if start >= l and end <= r:
            self.tree[node] += (end - start + 1) * val
            if start != end:
                self.lazy[2*node] += val
                self.lazy[2*node+1] += val
            return
        
        mid = (start + end) // 2
        self._update(start, mid, l, r, val, 2*node)
        self._update(mid+1, end, l, r, val, 2*node+1)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    
    def queryRange(self, l, r):
        return self._query(0, self.n - 1, l, r, 1)
    
    def _query(self, start, end, l, r, node):
        if start > r or end < l:
            return 0
        
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2*node] += self.lazy[node]
                self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0
        
        if start >= l and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left = self._query(start, mid, l, r, 2*node)
        right = self._query(mid+1, end, l, r, 2*node+1)
        return left + right

# Example usage
arr = [1, 2, 3, 4, 5]
st = SegmentTree(arr)
st.updateRange(1, 3, 2)  # arr becomes [1, 4, 5, 6, 5]
print("Query(0, 2):", st.queryRange(0, 2))  # 10
print("Query(2, 4):", st.queryRange(2, 4))  # 16
