# Tailwind safelist — dynamically constructed classes that static scanning can't pick up.
# _SPACING maps: none=0 xs=1 sm=2 md=4 lg=8 xl=12 2xl=20
# _RADIUS maps: sm=rounded-lg md=rounded-xl lg=rounded-2xl full=rounded-full
# fmt: off
_CLASSES = """
grid-cols-1 grid-cols-2 grid-cols-3 grid-cols-4
sm:grid-cols-1 sm:grid-cols-2 sm:grid-cols-3 sm:grid-cols-4
md:grid-cols-1 md:grid-cols-2 md:grid-cols-3 md:grid-cols-4
lg:grid-cols-1 lg:grid-cols-2 lg:grid-cols-3 lg:grid-cols-4
xl:grid-cols-1 xl:grid-cols-2 xl:grid-cols-3 xl:grid-cols-4
gap-0 gap-1 gap-2 gap-4 gap-8 gap-12 gap-20
p-0 p-1 p-2 p-4 p-8 p-12 p-20
px-0 px-1 px-2 px-4 px-8 px-12 px-20
py-0 py-1 py-2 py-4 py-8 py-12 py-20
pt-0 pt-1 pt-2 pt-4 pt-8 pt-12 pt-20
pb-0 pb-1 pb-2 pb-4 pb-8 pb-12 pb-20
my-0 my-1 my-2 my-4 my-8 my-12 my-20
items-start items-center items-end
justify-start justify-center justify-end justify-between
sm:gap-0 sm:gap-1 sm:gap-2 sm:gap-4 sm:gap-8 sm:gap-12 sm:gap-20
md:gap-0 md:gap-1 md:gap-2 md:gap-4 md:gap-8 md:gap-12 md:gap-20
lg:gap-0 lg:gap-1 lg:gap-2 lg:gap-4 lg:gap-8 lg:gap-12 lg:gap-20
sm:p-0 sm:p-1 sm:p-2 sm:p-4 sm:p-8 sm:p-12 sm:p-20
md:p-0 md:p-1 md:p-2 md:p-4 md:p-8 md:p-12 md:p-20
lg:p-0 lg:p-1 lg:p-2 lg:p-4 lg:p-8 lg:p-12 lg:p-20
sm:px-0 sm:px-1 sm:px-2 sm:px-4 sm:px-8 sm:px-12 sm:px-20
md:px-0 md:px-1 md:px-2 md:px-4 md:px-8 md:px-12 md:px-20
lg:px-0 lg:px-1 lg:px-2 lg:px-4 lg:px-8 lg:px-12 lg:px-20
sm:py-0 sm:py-1 sm:py-2 sm:py-4 sm:py-8 sm:py-12 sm:py-20
md:py-0 md:py-1 md:py-2 md:py-4 md:py-8 md:py-12 md:py-20
lg:py-0 lg:py-1 lg:py-2 lg:py-4 lg:py-8 lg:py-12 lg:py-20
sm:items-start sm:items-center sm:items-end
md:items-start md:items-center md:items-end
lg:items-start lg:items-center lg:items-end
sm:justify-start sm:justify-center sm:justify-end sm:justify-between
md:justify-start md:justify-center md:justify-end md:justify-between
lg:justify-start lg:justify-center lg:justify-end lg:justify-between
rounded-lg rounded-xl rounded-2xl rounded-full
text-xs text-sm text-base text-lg text-xl text-2xl text-3xl text-4xl text-5xl text-6xl
sm:text-xs sm:text-sm sm:text-base sm:text-lg sm:text-xl sm:text-2xl sm:text-3xl
md:text-xs md:text-sm md:text-base md:text-lg md:text-xl md:text-2xl md:text-3xl
lg:text-xs lg:text-sm lg:text-base lg:text-lg lg:text-xl lg:text-2xl lg:text-3xl
left-[25%] left-[50%] left-[75%]
"""
