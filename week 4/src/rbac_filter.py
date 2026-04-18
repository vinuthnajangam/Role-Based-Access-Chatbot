import json
import os
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RBACFilter:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, '..', 'config', 'role_hierarchy.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.role_hierarchy = self.config.get("hierarchy", {})
        self.dept_access = self.config.get("department_access", {})
        
        # Normalize dept access keys to lowercase for robust matching
        self.dept_access = {k.lower(): [d.lower() for d in v] for k, v in self.dept_access.items()}

    def get_accessible_departments(self, user_role):
        user_role = user_role.lower()
        return self.dept_access.get(user_role, [])

    def filter_by_role(self, user_role, search_results):
        """
        Filters search results based on user role.
        
        Args:
            user_role (str): The role of the user (e.g., 'finance', 'c-level')
            search_results (list): List of dicts with 'metadata' -> 'department'
            
        Returns:
            list: Filtered results
        """
        user_role = user_role.lower()
        allowed_depts = self.get_accessible_departments(user_role)
        
        filtered = []
        blocked_count = 0
        
        for result in search_results:
            # Safely get department, default to unknown
            doc_dept = result.get('metadata', {}).get('department', 'unknown')
            
            # Check if doc_dept is in allowed list (case-insensitive)
            if doc_dept.lower() in allowed_depts:
                filtered.append(result)
            else:
                blocked_count += 1
                
        logger.info(f"RBAC Filter: Role='{user_role}' | Allowed={len(filtered)} | Blocked={blocked_count}")
        return filtered

if __name__ == "__main__":
    # Test
    rbac = RBACFilter()
    
    sample_results = [
        {"id": "1", "metadata": {"department": "Finance"}},
        {"id": "2", "metadata": {"department": "HR"}},
        {"id": "3", "metadata": {"department": "General"}}
    ]
    
    print("Testing Finance User:")
    res = rbac.filter_by_role("finance", sample_results)
    for r in res: print(f"- {r['metadata']['department']}")
    
    print("\nTesting C-Level User:")
    res = rbac.filter_by_role("c-level", sample_results)
    for r in res: print(f"- {r['metadata']['department']}")
