"""
Health monitoring and system diagnostics for the workflow
"""

import os
import sys
import time
import psutil
import requests
from datetime import datetime
from typing import Dict, Any, List
from config import Config

class HealthMonitor:
    """System health monitoring and diagnostics"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def check_system_health(self) -> Dict[str, Any]:
        """Comprehensive system health check"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": time.time() - self.start_time,
            "system": self._check_system_resources(),
            "dependencies": self._check_dependencies(),
            "configuration": self._check_configuration(),
            "external_services": self._check_external_services(),
            "storage": self._check_storage(),
            "overall_status": "healthy"  # Will be updated based on checks
        }
    
    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            cpu_percent = psutil.cpu_percent(interval=1)
            
            return {
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_percent": memory.percent,
                    "status": "healthy" if memory.percent < 85 else "warning"
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_percent": round((disk.used / disk.total) * 100, 2),
                    "status": "healthy" if (disk.used / disk.total) < 0.9 else "warning"
                },
                "cpu": {
                    "usage_percent": cpu_percent,
                    "status": "healthy" if cpu_percent < 80 else "warning"
                }
            }
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def _check_dependencies(self) -> Dict[str, Any]:
        """Check if all required dependencies are available"""
        
        required_packages = [
            "tinytroupe",
            "openai",
            "flask", 
            "flask_cors",
            "python_dotenv",
            "pydantic",
            "requests",
            "jsonschema"
        ]
        
        available = []
        missing = []
        versions = {}
        
        for package in required_packages:
            try:
                module = __import__(package)
                available.append(package)
                
                # Try to get version
                if hasattr(module, '__version__'):
                    versions[package] = module.__version__
                
            except ImportError:
                missing.append(package)
        
        return {
            "available": available,
            "missing": missing,
            "versions": versions,
            "status": "healthy" if len(missing) == 0 else "error"
        }
    
    def _check_configuration(self) -> Dict[str, Any]:
        """Check configuration validity"""
        
        config_checks = {
            "openai_api_key": bool(Config.OPENAI_API_KEY),
            "openai_model": bool(Config.OPENAI_MODEL),
            "cache_dir_exists": os.path.exists(Config.TINYTROUPE_CACHE_DIR),
            "cache_dir_writable": os.access(Config.TINYTROUPE_CACHE_DIR, os.W_OK) if os.path.exists(Config.TINYTROUPE_CACHE_DIR) else False
        }
        
        all_valid = all(config_checks.values())
        
        return {
            "checks": config_checks,
            "status": "healthy" if all_valid else "error",
            "config_values": {
                "openai_model": Config.OPENAI_MODEL,
                "flask_port": Config.FLASK_PORT,
                "cache_dir": Config.TINYTROUPE_CACHE_DIR,
                "max_personas": Config.MAX_PERSONAS
            }
        }
    
    def _check_external_services(self) -> Dict[str, Any]:
        """Check external service connectivity"""
        
        services = {}
        
        # Check OpenAI API
        try:
            from openai import OpenAI
            client = OpenAI(api_key=Config.OPENAI_API_KEY)
            
            # Simple API test
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            
            services["openai"] = {
                "status": "healthy",
                "model": Config.OPENAI_MODEL,
                "response_time_ms": 0  # Could add timing
            }
            
        except Exception as e:
            services["openai"] = {
                "status": "error",
                "error": str(e)
            }
        
        return services
    
    def _check_storage(self) -> Dict[str, Any]:
        """Check storage and file system health"""
        
        directories = [
            Config.TINYTROUPE_CACHE_DIR,
            "logs",
            "exports"
        ]
        
        storage_status = {}
        
        for directory in directories:
            try:
                exists = os.path.exists(directory)
                writable = os.access(directory, os.W_OK) if exists else False
                
                # Check directory size if it exists
                size_mb = 0
                if exists:
                    total_size = 0
                    for dirpath, dirnames, filenames in os.walk(directory):
                        for filename in filenames:
                            filepath = os.path.join(dirpath, filename)
                            try:
                                total_size += os.path.getsize(filepath)
                            except:
                                pass
                    size_mb = round(total_size / (1024**2), 2)
                
                storage_status[directory] = {
                    "exists": exists,
                    "writable": writable,
                    "size_mb": size_mb,
                    "status": "healthy" if exists and writable else "warning"
                }
                
            except Exception as e:
                storage_status[directory] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return storage_status

class PerformanceMonitor:
    """Monitor workflow performance and timing"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation: str) -> float:
        """End timing and return duration"""
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            self.metrics[operation] = duration
            del self.start_times[operation]
            return duration
        return 0.0
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics"""
        return {
            "completed_operations": self.metrics,
            "active_operations": list(self.start_times.keys()),
            "total_operations": len(self.metrics)
        }

def run_health_check() -> Dict[str, Any]:
    """Run comprehensive health check"""
    
    print("🏥 Running System Health Check")
    print("=" * 30)
    
    monitor = HealthMonitor()
    health_report = monitor.check_system_health()
    
    # Print summary
    print(f"⏰ Timestamp: {health_report['timestamp']}")
    print(f"🕐 Uptime: {health_report['uptime_seconds']:.1f} seconds")
    
    # System resources
    if "system" in health_report and "error" not in health_report["system"]:
        system = health_report["system"]
        print(f"💾 Memory: {system['memory']['used_percent']:.1f}% used")
        print(f"💿 Disk: {system['disk']['used_percent']:.1f}% used")
        print(f"🖥️  CPU: {system['cpu']['usage_percent']:.1f}% used")
    
    # Dependencies
    if "dependencies" in health_report:
        deps = health_report["dependencies"]
        print(f"📦 Dependencies: {len(deps['available'])}/{len(deps['available']) + len(deps['missing'])} available")
        if deps["missing"]:
            print(f"   Missing: {', '.join(deps['missing'])}")
    
    # Configuration
    if "configuration" in health_report:
        config = health_report["configuration"]
        print(f"⚙️  Configuration: {config['status']}")
    
    # External services
    if "external_services" in health_report:
        services = health_report["external_services"]
        for service, status in services.items():
            print(f"🌐 {service.title()}: {status['status']}")
    
    return health_report

if __name__ == "__main__":
    report = run_health_check()
    
    # Save health report
    filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Health report saved to: {filename}")
    
    # Exit with appropriate code
    overall_healthy = all(
        component.get("status") == "healthy" 
        for component in report.values() 
        if isinstance(component, dict) and "status" in component
    )
    
    if overall_healthy:
        print("✅ System is healthy!")
        sys.exit(0)
    else:
        print("⚠️  System has issues - check the report")
        sys.exit(1)