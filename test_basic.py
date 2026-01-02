"""
基础测试 - 不依赖外部服务
测试代码结构和导入
"""
import sys
import os

# 添加backend到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """测试模块导入"""
    print("=" * 50)
    print("测试模块导入")
    print("=" * 50)
    
    errors = []
    
    try:
        from app.core.config import settings
        print("✓ config模块导入成功")
    except Exception as e:
        print(f"✗ config模块导入失败: {e}")
        errors.append(str(e))
    
    try:
        from app.core.database import Base, get_db
        print("✓ database模块导入成功")
    except Exception as e:
        print(f"✗ database模块导入失败: {e}")
        errors.append(str(e))
    
    try:
        from app.models import Case, User, Upload
        print("✓ models模块导入成功")
    except Exception as e:
        print(f"✗ models模块导入失败: {e}")
        errors.append(str(e))
    
    try:
        from app.services.case_service import CaseService
        print("✓ services模块导入成功")
    except Exception as e:
        print(f"✗ services模块导入失败: {e}")
        errors.append(str(e))
    
    try:
        from app.api.v1 import api_router
        print("✓ API路由导入成功")
    except Exception as e:
        print(f"✗ API路由导入失败: {e}")
        errors.append(str(e))
    
    return len(errors) == 0

def test_config():
    """测试配置"""
    print("\n" + "=" * 50)
    print("测试配置")
    print("=" * 50)
    
    try:
        from app.core.config import settings
        print(f"数据库URL配置: {'已设置' if hasattr(settings, 'DATABASE_URL') else '未设置'}")
        print(f"Redis URL配置: {'已设置' if hasattr(settings, 'REDIS_URL') else '未设置'}")
        return True
    except Exception as e:
        print(f"配置测试失败: {e}")
        return False

def test_models():
    """测试模型定义"""
    print("\n" + "=" * 50)
    print("测试数据模型")
    print("=" * 50)
    
    try:
        from app.models.case import Case
        from app.models.upload import Upload, UploadType
        from app.models.plan import Plan, PlanCode
        
        print(f"✓ Case模型: {Case.__tablename__}")
        print(f"✓ Upload模型: {Upload.__tablename__}")
        print(f"✓ Plan模型: {Plan.__tablename__}")
        print(f"✓ UploadType枚举: {list(UploadType)}")
        print(f"✓ PlanCode枚举: {list(PlanCode)}")
        return True
    except Exception as e:
        print(f"模型测试失败: {e}")
        return False

def test_services():
    """测试服务类"""
    print("\n" + "=" * 50)
    print("测试服务类")
    print("=" * 50)
    
    try:
        from app.services.pricing_engine import PricingEngine
        
        engine = PricingEngine()
        print(f"✓ PricingEngine初始化成功")
        print(f"  价格目录项目数: {len(engine.price_catalog.get('items', []))}")
        
        # 测试生成方案
        from app.models.plan import PlanCode
        test_requirements = {
            "workpiece": {"weight_range": "10-50kg"},
            "process": {"count": 2, "needs_flip": True}
        }
        
        plan_spec = engine.generate_plan_spec(PlanCode.P1, test_requirements)
        print(f"✓ 方案生成测试: {plan_spec['name']}")
        
        return True
    except Exception as e:
        print(f"服务测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有基础测试"""
    print("\n" + "=" * 50)
    print("开始基础测试")
    print("=" * 50)
    
    results = {}
    
    results['imports'] = test_imports()
    results['config'] = test_config()
    results['models'] = test_models()
    results['services'] = test_services()
    
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    for test_name, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {test_name}: {result}")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n✓ 所有基础测试通过！代码结构正常。")
    else:
        print("\n✗ 部分测试失败，请检查错误信息。")

if __name__ == "__main__":
    main()

