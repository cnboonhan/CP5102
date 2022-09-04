FROM node:slim

WORKDIR /usr/src/mockpass

RUN npm install @opengovsg/mockpass

ENV SHOW_LOGIN_PAGE=true
#ENV SINGPASS_ASSERT_ENDPOINT=https://localhost/singpass/assert

CMD ["npx", "mockpass"]
