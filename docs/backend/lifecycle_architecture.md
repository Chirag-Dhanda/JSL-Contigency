# Enterprise Dependency Injection & Application Lifecycle

**Purpose**: Manage application complexity by providing a strictly defined startup/shutdown sequence, avoiding tight coupling via Dependency Injection (IoC Container), and allowing loose communication via Event Dispatching.

## 1. Application Lifecycle (`core/lifecycle.py`)
All execution phases follow a deterministic sequence handled by the `ApplicationManager`:
1. `APP_STARTING` event dispatched.
2. Configuration Validated and Loaded (`CONFIG_LOADED`).
3. Services registered into DI Container (`MODULES_REGISTERED`).
4. Modules initialized asynchronously.
5. Application begins serving traffic (`APP_READY`).

During shutdown, modules are destructed in the reverse order of their registration.

## 2. Dependency Injection Container (`core/di.py`)
Replaces direct instantiation of shared classes (e.g. Database Pools, API Clients).
- **Singletons**: Persistent throughout the application lifecycle. `container.register_singleton(IMyService, MyServiceImpl())`
- **Transients**: Generates a new instance every time requested. `container.register_transient(IMyService, lambda: MyServiceImpl())`
- **Collision Protection**: Throw `SystemException` if a module attempts to register a service that already exists.
- **Resolution**: Retrieve using `container.resolve(IMyService)`.

## 3. Module System (`core/module.py`)
Every future business domain (Auth, SAP, Reporting) MUST be encapsulated into a Module inheriting `BaseModule`.
```python
class SAPModule(BaseModule):
    @property
    def name(self): return "SAP Integration"
    
    def register_services(self, container):
        container.register_singleton(SAPClient, RealSAPClient())
        
    async def initialize(self):
        # Connect to SAP
        pass
        
    async def shutdown(self):
        # Disconnect from SAP
        pass
```

## 4. Internal Events (`core/events.py`)
Allows domains to react to system changes without depending directly on each other.
```python
async def on_app_ready():
    print("App is ready!")

event_dispatcher.subscribe(ApplicationEvents.APP_READY, on_app_ready)
```
