CC = g++

CFLAGS = -std=c++11 -Wall

# !!! Change with your paths for cplex
INCLUDES = -I/home/filippo/Documents/Uni/2023/Tesi/ibm/cplex/include/ -I/home/filippo/Documents/Uni/2023/Tesi/ibm/concert/include/

LIB_DIRS = -L/home/filippo/Documents/Uni/2023/Tesi/ibm/concert/lib/x86-64_linux/static_pic -L/home/filippo/Documents/Uni/2023/Tesi/ibm/cplex/lib/x86-64_linux/static_pic

LIBS = -lilocplex -lconcert -lcplex -lm -lpthread -ldl

MARKOWITZ_SRCS = markowitz.cpp 
CDD_SRCS = cdd.cpp 

MARKOWITZ_TARGET = markowitz
CDD_TARGET = cdd

INSTANCES_FILE = run_instances.txt

INSTANCES := $(shell cat $(INSTANCES_FILE))


all: $(MARKOWITZ_TARGET) $(CDD_TARGET)

$(MARKOWITZ_TARGET): $(MARKOWITZ_SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $(LIB_DIRS) -o $(MARKOWITZ_TARGET) $(MARKOWITZ_SRCS) $(LIBS)

$(CDD_TARGET): $(CDD_SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $(LIB_DIRS) -o $(CDD_TARGET) $(CDD_SRCS) $(LIBS)

clean:
	rm -f $(MARKOWITZ_TARGET) $(CDD_TARGET)

rebuild: clean all

run: all
	for instance in $(INSTANCES); do \
		./$(MARKOWITZ_TARGET) "$$instance"; \
		./$(CDD_TARGET) "$$instance"; \
	done
