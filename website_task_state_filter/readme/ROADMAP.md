This module overwrites the portal_my_tasks controller function for the /my/tasks URL path. Modules that inherit or extend this function may not work as expected.

This limitation has been accepted because overwriting the function is the only efficient way to implement the required behavior for this module, and modules that inherit the portal_my_tasks controller are uncommon.
