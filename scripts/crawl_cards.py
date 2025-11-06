# scripts/crawl_cards.py

import sys
import os
import signal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection.card_crawler import CardCrawler

# 전역 변수
crawler = None

def signal_handler(sig, frame):
    """Ctrl+C 처리"""
    print('\n\n⚠️  Ctrl+C 감지! 안전하게 종료 중...')
    print(f'📍 현재까지 크롤링한 위치가 체크포인트에 저장되었습니다.')
    if crawler:
        crawler.close()
    sys.exit(0)


def main():
    global crawler  # 전역 변수 사용

    # Ctrl+C 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)

    print("=" * 60)
    print("카드 크롤러")
    print("=" * 60)

    # 체크포인트 확인
    checkpoint_file = './data/raw/checkpoint_CHK.json'
    has_checkpoint = os.path.exists(checkpoint_file)

    if has_checkpoint:
        import json
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
            last_index = checkpoint.get('last_index', 0)

        print(f"\n🔖 체크포인트 발견!")
        print(f"   마지막 저장: {last_index}번째 카드")
        resume = input("\n이어서 크롤링하시겠습니까? (y/n): ").lower()

        if resume == 'y':
            print(f"✅ {last_index + 1}번째 카드부터 재개합니다.")

            crawler = CardCrawler()
            try:
                csv_file = crawler.crawl_all_cards(
                    card_type='CHK',
                    test_mode=False
                )
                print(f"\n✅ 크롤링 완료!")
                print(f"📁 저장 위치: {csv_file}")
            except Exception as e:
                print(f"\n❌ 오류 발생: {str(e)}")
            finally:
                crawler.close()
            return

    # 테스트 모드 선택
    mode = input("\n모드 선택 (1: 테스트 10개, 2: 전체): ")

    if mode == "1":
        test_mode = True
        test_limit = 10
        print("\n🧪 테스트 모드 선택 (10개 카드만)")
    elif mode == "2":
        test_mode = False
        test_limit = None
        print("\n🚀 전체 크롤링 모드 선택")
    else:
        print("❌ 잘못된 입력입니다.")
        return

    # 카드 타입 선택
    card_type = input("\n크롤링할 카드 종류 (CHK: 체크카드, CRD: 신용카드): ").upper()

    if card_type not in ['CHK', 'CRD']:
        print("❌ 잘못된 입력입니다. CHK 또는 CRD를 입력하세요.")
        return

    # 수동 시작 옵션
    manual_start = None
    if not test_mode:
        manual_input = input("\n특정 위치부터 시작하시겠습니까? (번호 입력 또는 Enter): ")
        if manual_input.strip():
            try:
                manual_start = int(manual_input)
                print(f"🎯 {manual_start}번째 카드부터 시작합니다.")
            except:
                print("⚠️ 잘못된 입력입니다. 처음부터 시작합니다.")

    # 크롤러 실행
    crawler = CardCrawler()

    try:
        csv_file = crawler.crawl_all_cards(
            card_type=card_type,
            test_mode=test_mode,
            test_limit=test_limit,
            manual_start=manual_start
        )
        print(f"\n✅ 크롤링 완료!")
        print(f"📁 저장 위치: {csv_file}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()  # 상세 오류 출력

    finally:
        crawler.close()


if __name__ == "__main__":
    main()