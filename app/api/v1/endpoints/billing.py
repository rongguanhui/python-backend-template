from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import stripe
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.core.logger import logger

router = APIRouter()

stripe.api_key = settings.STRIPE_API_KEY  # 需要在 .env 加这个


@router.post("/webhook/stripe")
async def stripe_webhook(
        request: Request,
        stripe_signature: str = Header(None),
        db: AsyncSession = Depends(get_db)
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET  # 需要在 .env 加这个
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 处理支付成功事件
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email')

        if customer_email:
            logger.info(f"支付成功: {customer_email}")

            # 查找用户并开通 VIP
            result = await db.execute(select(User).filter(User.email == customer_email))
            user = result.scalars().first()

            if user:
                user.is_vip = True
                # 这里简单处理，实际应根据 plan 计算时间
                # user.vip_expire_at = datetime.now() + timedelta(days=30)
                await db.commit()

    return {"status": "success"}