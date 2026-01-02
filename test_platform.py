"""
平台测试脚本
测试后端API和基本功能
"""
import requests
import json
import time
import os

BASE_URL = "http://localhost:8000/api"

def test_health():
    """测试健康检查"""
    print("=" * 50)
    print("测试1: 健康检查")
    print("=" * 50)
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_create_case():
    """测试创建案件"""
    print("\n" + "=" * 50)
    print("测试2: 创建案件")
    print("=" * 50)
    try:
        data = {
            "title": "测试案件 - " + time.strftime("%Y%m%d_%H%M%S"),
            "industry": "制造业"
        }
        response = requests.post(f"{BASE_URL}/cases", json=data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 201:
            case_data = response.json()
            print(f"案件ID: {case_data['id']}")
            print(f"案件名称: {case_data['title']}")
            return case_data['id']
        else:
            print(f"错误响应: {response.text}")
            return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def test_upload_file(case_id, file_path, file_type="transcript"):
    """测试上传文件"""
    print("\n" + "=" * 50)
    print(f"测试3: 上传{file_type}文件")
    print("=" * 50)
    try:
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            # 创建一个测试文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("这是测试逐字稿内容\n")
                f.write("客户提到需要自动化生产线\n")
                f.write("工件重量范围：10-50kg\n")
                f.write("需要翻转工序\n")
            print(f"已创建测试文件: {file_path}")
        
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/plain')}
            response = requests.post(f"{BASE_URL}/cases/{case_id}/uploads", files=files)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 201:
            upload_data = response.json()
            print(f"上传ID: {upload_data['id']}")
            print(f"文件名: {upload_data['filename']}")
            print(f"类型: {upload_data['type']}")
            return True
        else:
            print(f"错误响应: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_list_uploads(case_id):
    """测试列出上传文件"""
    print("\n" + "=" * 50)
    print("测试4: 列出上传文件")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/cases/{case_id}/uploads")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            uploads = response.json()
            print(f"上传文件数量: {len(uploads)}")
            for upload in uploads:
                print(f"  - {upload['filename']} ({upload['type']})")
            return True
        else:
            print(f"错误响应: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_start_extraction(case_id):
    """测试开始提取"""
    print("\n" + "=" * 50)
    print("测试5: 开始需求提取")
    print("=" * 50)
    try:
        response = requests.post(f"{BASE_URL}/cases/{case_id}/extract")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            run_data = response.json()
            print(f"提取运行ID: {run_data['id']}")
            print(f"版本: {run_data['version']}")
            print(f"状态: {run_data['status']}")
            return run_data['id']
        else:
            print(f"错误响应: {response.text}")
            return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def test_get_extraction_status(run_id):
    """测试获取提取状态"""
    print("\n" + "=" * 50)
    print("测试6: 检查提取状态")
    print("=" * 50)
    try:
        max_wait = 60  # 最多等待60秒
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = requests.get(f"{BASE_URL}/cases/runs/{run_id}")
            if response.status_code == 200:
                run_data = response.json()
                status = run_data['status']
                print(f"当前状态: {status}")
                
                if status == 'completed':
                    print("✓ 提取完成！")
                    return True
                elif status == 'failed':
                    print("✗ 提取失败")
                    return False
                else:
                    print("等待中...")
                    time.sleep(3)
            else:
                print(f"错误响应: {response.text}")
                return False
        
        print("超时")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_get_requirements(case_id):
    """测试获取需求"""
    print("\n" + "=" * 50)
    print("测试7: 获取提取的需求")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/cases/{case_id}/requirements")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            req_data = response.json()
            print(f"运行ID: {req_data['run_id']}")
            print(f"需求数据键: {list(req_data['jsonb_data'].keys())}")
            if req_data.get('evidence'):
                print(f"证据数量: {len(req_data['evidence'])}")
            return True
        else:
            print(f"错误响应: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_generate_plans(case_id):
    """测试生成方案"""
    print("\n" + "=" * 50)
    print("测试8: 生成报价方案")
    print("=" * 50)
    try:
        response = requests.post(f"{BASE_URL}/cases/{case_id}/generate-plans")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            plans = response.json()
            print(f"方案数量: {len(plans)}")
            for plan in plans:
                print(f"  - {plan['plan_code']}: {plan['name']}")
                print(f"    报价项目数: {len(plan.get('quote_items', []))}")
            return True
        else:
            print(f"错误响应: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_list_documents(case_id):
    """测试列出文档"""
    print("\n" + "=" * 50)
    print("测试9: 列出生成的文档")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/cases/{case_id}/documents")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            docs = response.json()
            print(f"文档数量: {len(docs)}")
            for doc in docs:
                print(f"  - {doc['doc_type']}.{doc['format']}")
            return len(docs) > 0
        else:
            print(f"错误响应: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    """主测试流程"""
    print("\n" + "=" * 50)
    print("开始测试平台")
    print("=" * 50)
    
    results = {}
    
    # 测试1: 健康检查
    results['health'] = test_health()
    if not results['health']:
        print("\n❌ 后端服务未运行，请先启动后端服务")
        print("运行命令: cd backend && python run.py")
        return
    
    # 测试2: 创建案件
    case_id = test_create_case()
    if not case_id:
        print("\n❌ 无法创建案件，测试终止")
        return
    results['create_case'] = True
    
    # 测试3: 上传文件
    test_file = "test_transcript.txt"
    results['upload'] = test_upload_file(case_id, test_file)
    
    # 测试4: 列出上传
    results['list_uploads'] = test_list_uploads(case_id)
    
    # 测试5: 开始提取（如果LLM未配置，可能会失败）
    run_id = test_start_extraction(case_id)
    results['start_extraction'] = run_id is not None
    
    if run_id:
        # 测试6: 等待提取完成
        results['extraction_complete'] = test_get_extraction_status(run_id)
        
        if results['extraction_complete']:
            # 测试7: 获取需求
            results['get_requirements'] = test_get_requirements(case_id)
            
            # 测试8: 生成方案
            results['generate_plans'] = test_generate_plans(case_id)
            
            # 测试9: 生成文档（需要等待）
            print("\n等待文档生成...")
            time.sleep(5)
            results['list_documents'] = test_list_documents(case_id)
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    for test_name, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {test_name}: {result}")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    print(f"\n总计: {passed}/{total} 测试通过")

if __name__ == "__main__":
    main()

