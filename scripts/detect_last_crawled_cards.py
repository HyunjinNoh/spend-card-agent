import pandas as pd
import json
import os


def check_crawling_progress():
    """
    현재 크롤링 진행 상황 확인
    """
    # CHK 카드 크롤링한 CSV 파일 찾기
    csv_dir = '../data/raw'
    csv_files = [f for f in os.listdir(csv_dir) if f.startswith('cards_raw_CHK') and f.endswith('.csv')]

    if not csv_files:
        print("❌ CSV 파일을 찾을 수 없습니다!")
        return

    # 가장 최근 파일
    latest_csv = sorted(csv_files)[-1]
    csv_path = os.path.join(csv_dir, latest_csv)

    print("=" * 60)
    print(f"📄 CSV 파일: {latest_csv}")
    print("=" * 60)

    # CSV 읽기
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    # 통계
    total_rows = len(df)
    unique_cards = df['card_id'].unique()
    saved_count = len(unique_cards)

    print(f"\n📊 통계:")
    print(f"   총 행 수: {total_rows:,}개")
    print(f"   저장된 카드: {saved_count}개")
    print(f"   평균 혜택/카드: {total_rows / saved_count:.1f}개")

    # 마지막 5개 카드
    print(f"\n🔖 마지막 5개 카드:")
    last_5 = unique_cards[-5:]
    for i, card_id in enumerate(last_5, saved_count - 4):
        benefits_count = len(df[df['card_id'] == card_id])
        print(f"   {i}번째: 카드 ID {card_id} (혜택 {benefits_count}개)")

    # 체크포인트 확인
    checkpoint_file = os.path.join(csv_dir, 'checkpoint_CHK.json')
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)

        print(f"\n📍 체크포인트:")
        print(f"   last_index: {checkpoint.get('last_index', 0)}")
        print(f"   timestamp: {checkpoint.get('timestamp', 'N/A')}")

        # 불일치 확인
        if checkpoint.get('last_index', 0) != saved_count:
            print(f"\n⚠️  불일치 발견!")
            print(f"   체크포인트: {checkpoint.get('last_index')}번")
            print(f"   실제 저장: {saved_count}번")

    # 수정 제안
    print(f"\n💡 다음 행동:")
    print(f"   1. 체크포인트를 {saved_count}으로 수정")
    print(f"   2. {saved_count + 1}번째 카드부터 재시작")

    # 자동 수정 옵션
    if input("\n체크포인트를 자동으로 수정하시겠습니까? (y/n): ").lower() == 'y':
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)

        checkpoint['last_index'] = saved_count
        checkpoint['csv_filename'] = csv_path

        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)

        print(f"✅ 체크포인트 수정 완료!")
        print(f"   last_index = {saved_count}")
        print(f"   다음 실행 시 {saved_count + 1}번째 카드부터 시작됩니다.")


if __name__ == "__main__":
    check_crawling_progress()